from unittest.mock import MagicMock

import pytest
from docker.errors import APIError

from veracity_harness.sandbox import DockerArena


def test_container_is_owned_before_start_can_fail(monkeypatch, tmp_path):
    client = MagicMock()
    client.api._proxy_configs = {"no_proxy": "localhost,original.internal"}
    container = client.containers.create.return_value
    container.start.side_effect = APIError("Fixture startup failure")
    monkeypatch.setattr("veracity_harness.sandbox.docker.from_env", lambda **kwargs: client)
    arena = DockerArena("partial-start-fixture")
    with pytest.raises(APIError):
        arena.start_gateway(tmp_path, "Interface")
    arena.close()
    container.remove.assert_called_once_with(force=True)
    client.close.assert_called_once()


def test_bind_mounted_staging_outlives_every_container_that_mounts_it(monkeypatch):
    # Deleting a bind-mount source before its container is removed crashed
    # Docker Desktop's file sharing and, with it, containerd.
    client = MagicMock()
    client.api._proxy_configs = {"no_proxy": "localhost,original.internal"}
    monkeypatch.setattr("veracity_harness.sandbox.docker.from_env", lambda **kwargs: client)
    arena = DockerArena("staging-fixture")
    staging = arena.staging
    seen = []
    client.containers.create.return_value.remove.side_effect = lambda **kwargs: seen.append(
        staging.exists()
    )
    (staging / "gateway").mkdir()
    (staging / "juror-1").mkdir()
    gateway = arena.start_gateway(staging / "gateway", "Interface")
    arena.start_participant("juror-1", staging / "juror-1", gateway)
    arena.close()
    assert seen == [True, True]
    assert not staging.exists()


def test_staging_is_removed_even_when_container_cleanup_fails(monkeypatch):
    client = MagicMock()
    client.api._proxy_configs = {"no_proxy": "localhost,original.internal"}
    client.containers.create.return_value.remove.side_effect = APIError("Fixture failure")
    monkeypatch.setattr("veracity_harness.sandbox.docker.from_env", lambda **kwargs: client)
    arena = DockerArena("staging-failure-fixture")
    arena.start_gateway(arena.staging, "Interface")
    with pytest.raises(RuntimeError):
        arena.close()
    assert not arena.staging.exists()


def test_every_resource_carries_the_harness_run_label_for_cleanup(monkeypatch):
    client = MagicMock()
    client.api._proxy_configs = {"no_proxy": "localhost,original.internal"}
    monkeypatch.setattr("veracity_harness.sandbox.docker.from_env", lambda **kwargs: client)
    arena = DockerArena("node-3f9a1c2b7d4e", "run-abc123def456")
    (arena.staging / "gateway").mkdir()
    (arena.staging / "juror-1").mkdir()
    gateway = arena.start_gateway(arena.staging / "gateway", "Interface")
    arena.start_participant("juror-1", arena.staging / "juror-1", gateway)
    arena.create_shared_volume()
    label = {"veracity.session": "run-abc123def456"}
    for call in client.containers.create.call_args_list:
        assert label.items() <= call.kwargs["labels"].items()
        assert call.kwargs["environment"]["NO_PROXY"] == (
            "localhost,original.internal,veracity-api,host.docker.internal"
        )
    assert label.items() <= client.networks.create.call_args.kwargs["labels"].items()
    assert label.items() <= client.volumes.create.call_args.kwargs["labels"].items()
    arena.close()
