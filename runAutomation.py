import json
import time
import requests
from actions_toolkit import core

def main():
  iap_instance = core.get_input("IAP_INSTANCE")
  iap_token = core.get_input("IAP_TOKEN")
  api_endpoint = core.get_input("API_ENDPOINT")
  api_endpoint_body = core.get_input("API_ENDPOINT_BODY")
  timeout = int(core.get_input("TIMEOUT"))
  no_of_attempts = int(core.get_input("NO_OF_ATTEMPTS"))
  job_status = core.get_input("JOB_STATUS")
  count = 0

  if(iap_instance.endswith('/')):
    iap_instance=iap_instance[:-1]
  
  if(api_endpoint.startswith('/')):
    api_endpoint=api_endpoint[1:]

  try:
    #check the status of the job and return the output (IAP release <= 2021.1)
    def job_status_221(job_id,iap_instance,iap_token,count,no_of_attempts,timeout):
      response=requests.get(iap_instance+'/operations-manager/jobs/'+job_id+'?token='+iap_token)
      if (response.status_code!=200):
        response.raise_for_status()
      print('JOB Status:',response.json()["data"]["status"])

      if (response.json()["data"]["status"] == "running" and count < no_of_attempts):
        time.sleep(timeout)
        count=count+1
        job_status_221(job_id,iap_instance,iap_token,count,no_of_attempts,timeout)

      elif (response.json()["data"]["status"] == "complete"):
        output=response.json()["data"]["variables"]
        core.set_output("results",output)

      elif (response.json()["data"]["status"] == "canceled"):
        core.set_failed("Job Canceled")

      elif (response.json()["data"]["status"] == "error"):
        core.set_failed(response.json()["data"]["error"])

      else:
        core.set_failed("Job Timed out based upon user defined timeout and no_of_attempts")

    #check the status of the job and return the output (IAP release > 2021.1)
    def job_status_211(job_id,iap_instance,iap_token,count,no_of_attempts,timeout):
      response=requests.get(iap_instance+'/workflow_engine/job/'+job_id+'/details?token='+iap_token)
      if (response.status_code!=200):
        response.raise_for_status()
      print('JOB Status',response.json()["status"])

      if (response.json()["status"] == "running" and count < no_of_attempts):
        time.sleep(timeout)
        count=count+1
        job_status_211(job_id,iap_instance,iap_token,count,no_of_attempts,timeout)

      elif (response.json()["status"] == "complete"):
        result=requests.get(iap_instance+'/workflow_engine/job/'+job_id+'/output?token='+iap_token)
        if (result.status_code!=200):
          result.raise_for_status()
        core.set_output("results",result.json())

      elif (response.json()["status"] == "canceled"):
        core.set_failed("Job Canceled")

      elif (response.json()["status"] == "error"):
        core.set_failed(response.json()["error"])

      else:
        core.set_failed("Job Timed out based upon user defined timeout and no_of_attempts")

    def start_job(iap_instance):
      #API call to get IAP release
      release=requests.get(iap_instance+'/health/server',params={'token':iap_token})
      if (release.status_code!=200):
        release.raise_for_status()
      iap_release=release.json()["release"][0:release.json()["release"].rindex(".")]

      #API call to start API Endpoint trigger
      response=requests.post(iap_instance+'/operations-manager/triggers/endpoint/'+api_endpoint+'?token='+iap_token,json=json.loads(api_endpoint_body))
      if (response.status_code!=200):
        response.raise_for_status()
      if bool(int(job_status)) is True:
        if(float(iap_release)<=2021.1):
          job_status_211(response.json()["_id"],iap_instance,iap_token,count,no_of_attempts,timeout)
        else:
          job_status_221(response.json()["data"]["_id"],iap_instance,iap_token,count,no_of_attempts,timeout)
      else:
        if(float(iap_release)<=2021.1):
          core.set_output("results",response.json()["variables"])
        else:
          core.set_output("results",response.json()["data"]["variables"])
        

    start_job(iap_instance)
  except requests.exceptions.RequestException as err:
    core.set_failed(err)

if __name__ == "__main__":
    main()
