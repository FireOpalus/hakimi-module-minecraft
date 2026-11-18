"""Connect the Minecraft module to the authenticated domestic node."""

from hakimi.modules.mc_node import MinecraftNodeAdapter
from hakimi.modules.minecraft_slot import MinecraftSlotModule


def create_module(service):
    transport = service.node_transport
    module = MinecraftSlotModule(
        service.s,
        world_state=service.world_state,
        node_online=lambda: service.node_transport.connected(),
    )
    adapter = MinecraftNodeAdapter(module, lambda: service.node_transport, service.background)
    module.remote_dispatcher = adapter.dispatch
    if getattr(transport, "on_event", None) is None:
        transport.on_event = adapter.on_event
    if getattr(transport, "on_state", None) is None:
        transport.on_state = adapter.on_state
    return module
