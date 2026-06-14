from transformation_timeline import TransformationTimelineEngine

timeline = TransformationTimelineEngine.build(
    current_ipe=54,
    target_ipe=90
)

print(timeline)
