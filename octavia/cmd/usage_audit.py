# Copyright 2021 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from octavia.api.v2.types import load_balancer as lb_types
from octavia.common import context
from octavia.common import rpc
from octavia.common import service as octavia_service
from octavia.db import repositories


def main():
    octavia_service.prepare_service(sys.argv)

    ctx = context.Context()
    repos = repositories.Repositories()
    notifier = rpc.get_notifier()

    lbs, _ = repos.load_balancer.get_all(ctx.session, show_deleted=False)
    for lb in lbs:
        result = lb_types.LoadBalancerFullResponse.from_data_model(lb)
        notifier.info(ctx, 'octavia.loadbalancer.exists', result.to_dict())
