#!/usr/bin/env python3
"""Standalone simulation of reconcile-before-retry workflow recovery.

This file demonstrates the production design semantics with synthetic data. It is
not copied production source and performs no network, model, or filesystem writes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class InMemoryBroker:
    """Commit idempotent effects and simulate one lost acknowledgement."""

    effects: dict[str, dict[str, Any]] = field(default_factory=dict)
    dispatch_attempts: int = 0
    lose_first_acknowledgement: bool = True

    def find_effect(self, idempotency_key: str) -> dict[str, Any] | None:
        return self.effects.get(idempotency_key)

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        key = str(request["idempotency_key"])
        existing = self.find_effect(key)
        if existing is not None:
            return existing

        self.dispatch_attempts += 1
        payload = {
            "schema": "kent.research_brief.v1",
            "topic": request["topic"],
            "data_class": "public",
            "claims": [
                {
                    "text": "Ambiguous outcomes must be reconciled before retry.",
                    "evidence": "synthetic://portfolio-demo",
                }
            ],
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        effect = {
            "artifact_hash": "sha256:"
            + hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
            "payload": payload,
        }
        self.effects[key] = effect  # The authoritative effect commits first.

        if self.lose_first_acknowledgement:
            self.lose_first_acknowledgement = False
            raise TimeoutError("simulated response loss after Broker commit")
        return effect


@dataclass
class WorkflowRun:
    request: dict[str, Any]
    status: str = "pending"
    artifact_hash: str | None = None
    reconciled_before_retry: bool = False
    events: list[str] = field(default_factory=list)


class WorkflowCoordinator:
    def __init__(self, broker: InMemoryBroker) -> None:
        self.broker = broker

    def start(self, request: dict[str, Any]) -> WorkflowRun:
        self._validate(request)
        run = WorkflowRun(request=request, status="running")
        run.events.extend(["request_validated", "budget_reserved"])
        try:
            effect = self.broker.dispatch(request)
        except TimeoutError:
            run.status = "waiting_for_agent"
            run.events.append("dispatch_outcome_ambiguous")
            return run
        return self._complete(run, effect)

    def resume(self, run: WorkflowRun) -> WorkflowRun:
        if run.status != "waiting_for_agent":
            raise ValueError("only a waiting workflow may be resumed")

        key = str(run.request["idempotency_key"])
        committed = self.broker.find_effect(key)
        if committed is not None:
            run.reconciled_before_retry = True
            run.events.append("committed_effect_reconciled")
            return self._complete(run, committed)

        # A real coordinator may dispatch here only after the authoritative check.
        effect = self.broker.dispatch(run.request)
        return self._complete(run, effect)

    @staticmethod
    def _validate(request: dict[str, Any]) -> None:
        expected = {
            "workflow_definition",
            "idempotency_key",
            "topic",
            "data_class",
            "max_dispatches",
        }
        if set(request) != expected:
            raise ValueError("request contract is not closed")
        if request["workflow_definition"] != "pepper-kent-research-v1":
            raise ValueError("unknown workflow definition")
        if request["data_class"] != "public" or request["max_dispatches"] != 1:
            raise ValueError("demo permits one public dispatch")

    @staticmethod
    def _complete(
        run: WorkflowRun, effect: dict[str, Any]
    ) -> WorkflowRun:
        run.artifact_hash = str(effect["artifact_hash"])
        run.status = "completed"
        run.events.extend(["artifact_validated", "budget_settled", "completed"])
        return run


def main() -> None:
    request_path = Path(__file__).with_name("synthetic_request.json")
    request = json.loads(request_path.read_text(encoding="utf-8"))

    broker = InMemoryBroker()
    coordinator = WorkflowCoordinator(broker)
    run = coordinator.start(request)
    print(f"start_status={run.status}")

    run = coordinator.resume(run)
    print(f"resume_status={run.status}")
    print(f"dispatch_attempts={broker.dispatch_attempts}")
    print(
        "reconciled_before_retry="
        + str(run.reconciled_before_retry).lower()
    )
    print(f"artifact_hash={run.artifact_hash}")

    assert run.status == "completed"
    assert broker.dispatch_attempts == 1
    assert run.reconciled_before_retry is True
    assert run.artifact_hash is not None


if __name__ == "__main__":
    main()
