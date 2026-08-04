from inmotion.api import InMotionEvents, InMotionSession
from inmotion.models import (
    DataStreamFilterModel,
    DataStreamSummaryModel,
    EventCreatorModel,
    EventDetailsModel,
    EventLocationSummaryModel,
    EventNearbyFilterModel,
    EventUpdateModel,
)
from inmotion.utils import request_json, stringify


class InMotionEventsImpl(InMotionEvents):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/events"

    def create_event(self, event: EventCreatorModel) -> EventDetailsModel:
        event_data = stringify(event)
        return request_json('POST', self._prefix_path,
                             self._session.build_headers(content=event_data),
                             event_data,
                             'Failed to create event',
                             EventDetailsModel)

    def update_event(self, key: str, event: EventUpdateModel) -> EventDetailsModel:
        event_data = stringify(event)
        return request_json('PUT', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=event_data),
                             event_data,
                             'Failed to update event',
                             EventDetailsModel)

    def find_event(self, key: str) -> EventDetailsModel:
        return request_json('GET', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve event',
                             EventDetailsModel)

    def delete_event(self, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete event')

    def unlock_event(self, key: str) -> None:
        request_json('POST', f"{self._prefix_path}/{key}/unlock",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to unlock event')

    def find_events(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamSummaryModel]:
        filter_data = stringify(data_stream_filter)
        return request_json('POST', f"{self._prefix_path}/search",
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to find events',
                             DataStreamSummaryModel, many=True)

    def find_nearby_events(self, nearby_filter: EventNearbyFilterModel) -> list[EventLocationSummaryModel]:
        filter_data = stringify(nearby_filter)
        return request_json('POST', f"{self._prefix_path}/nearby",
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to find nearby events',
                             EventLocationSummaryModel, many=True)
