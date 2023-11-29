from api import *
from metrics import *
from config import get_config,get_args

args = get_args()
config_path = args.config
hw_host,hw_port,hw_username,hw_password,account_list = get_config(config_path)
def poolInfo(Fusion):
    global poolId
    global poolName
    data = Fusion.get_pool_info()
    for storagePools in data['storagePools']:
        poolId = storagePools['poolId']
        poolName = storagePools['poolName']
        totalCapacity = storagePools['totalCapacity']
        usedCapacity = storagePools['usedCapacity']
        poolStatus = storagePools['poolStatus']
        hw_nodepool_status.labels(id=poolId,name=poolName).set(poolStatus)
        hw_nodepool_total_hdd_cap.labels(id=poolId,name=poolName).set(totalCapacity)
        hw_nodepool_used_hdd_cap.labels(id=poolId,name=poolName).set(usedCapacity)
def accountInfo(Fusion,account_name):
    data = Fusion.get_account_info(account_name)
    for info in data:
        accountId = info['accountId']
        quotaCapacity = info['quotaCapacity']
        SpaceSize = info['SpaceSize']
        Quota = info['Quota']
        BucketCount = info['BucketCount']
        ObjectCount = info['ObjectCount']
        hw_account_id.labels(id=accountId).set(1)
        hw_account_quotaCapacity.labels(id=accountId).set(quotaCapacity)
        hw_account_SpaceSize.labels(id=accountId).set(SpaceSize)
        hw_account_Quota.labels(id=accountId).set(Quota)
        hw_account_BucketCount.labels(id=accountId).set(BucketCount)
        hw_account_ObjectCount.labels(id=accountId).set(ObjectCount)

def clusterReadWriteBan(Fusion):
    bandwith_data = Fusion.get_cluster_performance()
    for bandwith in bandwith_data['data']:
        indicatorValues = bandwith['indicatorValues']
        if bandwith['indicator'] == '123':
            hw_cluster_read_bandwidth.labels(id=poolId,name=poolName).set(indicatorValues)
        elif bandwith['indicator'] == '124':
            hw_cluster_write_bandwidth.labels(id=poolId,name=poolName).set(indicatorValues)
def api2metrics():
    account_name = account_list
    clear_metrics()
    Fusion = FusionStorage(host=hw_host,port=hw_port,username=hw_username,password=hw_password)
    Fusion.login()
    poolInfo(Fusion)
    accountInfo(Fusion,account_name)
    clusterReadWriteBan(Fusion)
    Fusion.logout()

