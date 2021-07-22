# "What's New On Azure" PPTX generator

This repository provides a simple Python-based Azure Function that can be used to generate a PowerPoint file that contains items published on the Azure Updates website (https://azure.microsoft.com/updates/) within a specified date range.

The implementation relies on the RSS feed for the website as its data source and the resulting PowerPoint is split into 'Preview' and 'GA' sections.

# Running locally

You can run this solution locally if you wish, though you will still require access to an Azure storage account or emulator.

The solution was built using Python 3.8 (on Ubuntu via WSL) and Visual Studio Code with it's excellent Python extensions. It hasn't been tested on a Windows platform, but should work with a path change for the `LocalTempFilePath` configuration item.

Define the following `local.settings.json` file in order to get the Functions running.

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "FUNCTION_STORAGE_ACCOUNT",
    "LocalTempFilePath": "/tmp/",
    "UpdatesURL": "https://azure.microsoft.com/updates/feed/",
    "PowerPointAccountConnection": "DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT;AccountKey=YOUR_KEY",
    "PowerPointContainer": "updatefiles",
    "PowerPointStorageAccount": "YOUR_ACCOUNT",
    "PowerPointStorageKey": "YOUR_KEY",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

# Deploy to Azure

You will need an Azure Storage Account, Azure Function (Comsumption Plan is perfect). When creating the Function you can elect to create the Application Insights instance to go along with it as well, though this is not strictly required.

Once you have this setup you can then extract the publishing profile for the Azure Function which can be achieved via either the Azure Portal (open the Function and download the profile by clicking 'Get publish profile' on the Overview screen) or via the Azure CLI by using the [az webapp deployment list-publishing-profiles](https://docs.microsoft.com/en-us/cli/azure/webapp/deployment?view=azure-cli-latest#az_webapp_deployment_list_publishing_profiles) command.

Add all the text from the downloaded profile to a Secret in your GitHub repository and ensure that the GitHub Action references this Secret correctly when publishing to Azure.

# Invoking the Function

Use a web browser and open the URL as shown below. 

https://YOUR-FUNC-APP.azurewebsites.net/api/GeneratePresentation?code=YOUR-FUNC-KEY&start=2021-06-20&end=2021-06-30

'start' parameter is required and should be in YYYY-MM-DD format. This is the oldest date to pull records from.
'end' parameter is optional, but if supplied should also be in YYYY-MM-DD format. This is the most recent date you want to pull records from.

The Function key isn't required for local debugging. For deployed Functions you can retrieve the Function Key from the [Azure Portal or via other APIs](https://docs.microsoft.com/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=csharp#obtaining-keys). 

There is also a Timer Function which runs every Sunday at 11pm to purge any generated PowerPoint files from storage.

# Known Limitations

The source RSS feed only holds ~60 days of announcements (or a fixed number of annoucements), so if you try and query before then you will get no results.