from oslo_log import log as logging
from octavia.common import context
from octavia.common import rpc
from octavia.api.v2.types import load_balancer as lb_types
from taskflow import task

LOG = logging.getLogger(__name__)

class BaseNotificationTask(task.Task):
    event_type = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rpc_notifier = rpc.get_notifier()

    def execute(self, loadbalancer):
        ctx = context.Context(project_id=loadbalancer.project_id)
        result = lb_types.LoadBalancerFullResponse.from_data_model(
            loadbalancer)
        LOG.info(f"Sending rpc notification: {self.event_type} {str(result.to_dict())}")
        self._rpc_notifier.info(
            ctx,
            self.event_type,
            result.to_dict()
        )

class SendUpdateNotification(BaseNotificationTask):
    event_type = 'octavia.loadbalancer.update.end'


class SendCreateNotification(BaseNotificationTask):
    event_type = 'octavia.loadbalancer.create.end'

class SendDeleteNotification(BaseNotificationTask):
    event_type = 'octavia.loadbalancer.delete.end'
