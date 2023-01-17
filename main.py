import os
import json
import time
import requests
from actions_toolkit import core

def main():
  IAP_INSTANCE = os.environ["IAP_INSTANCE"]
  IAP_TOKEN = os.environ["IAP_TOKEN"]
  API_ENDPOINT = os.environ["API_ENDPOINT"]
  API_ENDPOINT_BODY = os.environ["API_ENDPOINT_BODY"]
  TIMEOUT = int(os.environ["TIMEOUT"])
  NO_OF_ATTEMPTS = int(os.environ["NO_OF_ATTEMPTS"])
  JOB_STATUS = os.environ["JOB_STATUS"]

  count=0
  try:
    def jobStatus221(job_id,IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT):
      response=requests.get(IAP_INSTANCE+'/operations-manager/jobs/'+job_id+'?token='+IAP_TOKEN)
      if (response.status_code!=200):
        response.raise_for_status()
      print('JOB Status:',response.json()["data"]["status"])

      if (response.json()["data"]["status"] == "running" and count < NO_OF_ATTEMPTS):
        time.sleep(TIMEOUT)
        count=count+1
        jobStatus221(job_id,IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT)

      elif (response.json()["data"]["status"] == "complete"):
        output=response.json()["data"]["variables"]
        print(f"::set-output name=results::{output}")

      elif (response.json()["data"]["status"] == "canceled"):
        core.set_failed("Job Canceled")

      elif (response.json()["data"]["status"] == "error"):
        core.set_failed(response.json()["data"]["error"])

      else:
        core.set_failed("Job Timeout")

    def jobStatus211(job_id,IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT):
      print(job_id)
      response=requests.get(IAP_INSTANCE+'/workflow_engine/job/'+job_id+'/details?token='+IAP_TOKEN)
      if (response.status_code!=200):
        response.raise_for_status()
      print('JOB Status',response.json()["status"])

      if (response.json()["status"] == "running" and count < NO_OF_ATTEMPTS):
        time.sleep(TIMEOUT)
        count=count+1
        jobStatus211(job_id,IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT)

      elif (response.json()["status"] == "complete"):
        result=requests.get(IAP_INSTANCE+'/workflow_engine/job/'+job_id+'/output?token='+IAP_TOKEN)
        if (result.status_code!=200):
          result.raise_for_status()
        print(f"::set-output name=results::{result.json()}")

      elif (response.json()["status"] == "canceled"):
        print(response.json())
        core.set_failed("Job Canceled")

      elif (response.json()["status"] == "error"):
        core.set_failed(response.json()["error"])

      else:
        core.set_failed("Job Timeout")

    def startJob(IAP_INSTANCE):
      release=requests.get(IAP_INSTANCE+'/health/server',params={'token':IAP_TOKEN})
      if (release.status_code!=200):
        release.raise_for_status()
      iapRelease=release.json()["release"][0:release.json()["release"].rindex(".")]

      
      response=requests.post(IAP_INSTANCE+'/operations-manager/triggers/endpoint/'+API_ENDPOINT+'?token='+IAP_TOKEN,json=json.loads(API_ENDPOINT_BODY))
      # response.raise_for_status()
      if (response.status_code!=200):
        response.raise_for_status()
      if JOB_STATUS==True:
        if(iapRelease=="2021.1"):
          jobStatus211(response.json()["_id"],IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT)
        elif (iapRelease=="2021.2" or iapRelease=="2022.1"):
          jobStatus221(response.json()["data"]["_id"],IAP_INSTANCE,IAP_TOKEN,count,NO_OF_ATTEMPTS,TIMEOUT)
        else:
          core.set_failed("This Github Action doesn't support IAP release " + iapRelease)
        

    startJob(IAP_INSTANCE)
  except requests.exceptions.RequestException as err:
    core.set_failed(err)

if __name__ == "__main__":
    main()