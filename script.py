import boto3, sys

def performAction(action):
  print('Action type => ', action)
  client = boto3.resource('ec2',region_name='us-east-1')
  filteredInstances = []
  instances = [i for i in client.instances.all()]
  for i in instances:
    if i.tags is not None:
      if 'role' not in [t['Key'] for t in i.tags]:
        if 'jenkins' not in [t['Value'] for t in i.tags]:
          filteredInstances.append(i.instance_id)

  client = boto3.client('ec2',region_name='us-east-1')
  response = []
  instances = []
  if(action == 'start'):
    response = client.start_instances(InstanceIds=filteredInstances)
    instances = response["StartingInstances"]
    instances = [res["InstanceId"] for res in instances]
    return instances
  
  if(action == 'stop'):
    response = client.stop_instances(InstanceIds=filteredInstances)
    instances = response["StoppingInstances"]
    instances = [res["InstanceId"] for res in instances]
    return instances

try:
  action = sys.argv[1]
  match action:
    case 'start':
      instances = performAction('start')
      print('Sucessfully started the instances => ', instances)
    case 'stop':
      instances = performAction('stop')
      print('Sucessfully stopped the instances => ', instances)
except Exception as e:
  print(e)
finally:
  print('Finished processing')
