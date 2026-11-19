"""Public learning events that can supply a building idea."""

import re

from hakimi.life_rules import Reaction
from hakimi.world_state import MilestoneEvent

_MC_THEME = re.compile(
    r"我的世界|minecraft|\bmc\b|红石|生电|建筑教程|生存建筑|刷铁机|下界|末地|苦力怕", re.I
)


def build_from_video(event: MilestoneEvent) -> Reaction | None:
    if event.payload.get("private_first"):
        return None
    if event.payload.get("activity_kind") != "video_learning" and (
        event.source_module != "bilibili_surf"
        or event.event_type not in {"bili_video_watched", "bili_mc_inspiration"}
    ):
        return None
    topic = str(event.payload.get("title", ""))
    if event.event_type == "bili_mc_inspiration" or _MC_THEME.search(
        topic + " " + str(event.payload.get("summary", ""))
    ):
        return Reaction(
            "mc.build_plan",
            "刚刷到对胃口的 MC 视频，顺手记下想搭的建造灵感",
            ttl=7200,
            arguments={"topic": topic[:80]},
            legacy_module="minecraft",
            legacy_verb="build_plan",
        )
    return None
