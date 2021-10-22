---
title: Microsoft Azure Administrator (AZ-104) Notes
tags:
- blueteam
- technology
- notes
image: /images/azure/info.png
---

Moving to our next course in the series...(drumroll please) Microsoft Azure Administrator! We will need to start with a pre-requisite course.

<!--more-->

# Pre-requisite

Tasks of an azure admin:

    Deploying dozens or hundreds of resources at a time.
    Configuring individual services using scripts.
    Viewing rich reports across usage, health, costs, and more.

Ways an admin can do all this stuff:
- azure portal (we saw a lot of it in the fundamentals course)
- azure cloudshell: a browser based command line tool. you can use either bash or powershell. is temporary, has integrate hui text editor, authenticates automatically, timeout after 20 min of inactivity, Persists $HOME using a 5-GB image held in your file share.
- azure powershell: Interact with your resources using powershell style commands. comes in interactive mode and scripting mode. 
- azure cli: Interact with your resource using bash/terminal style commands. again comes in interactive and scripting mode.

First thing to start using azure on your local powershell is "Connect-AzAccount" command.

## Resource manager benefits

Azure Resource Manager enables you to work with the resources in your solution as a group. You can deploy, update, or delete all the resources for your solution in a single, coordinated operation. You use a template for deployment and that template can work for different environments such as testing, staging, and production.

<img src="/images/azureadmin/manager.png">

template - A JavaScript Object Notation (JSON) file that defines one or more resources to deploy to a resource group. It also defines the dependencies between the deployed resources. The template can be used to deploy the resources consistently and repeatedly.

Resource provider - resource provider offers a set of resources and operations for working with an Azure service. for ex Microsoft.KeyVault is a resource provider for keyvault service.

The name of a resource type is in the format: {resource-provider}/{resource-type}

[Resource Groups facts and uses](https://docs.microsoft.com/en-us/learn/modules/use-azure-resource-manager/4-create-resource-groups)

You need to specify resource group location (even though the resources inside it can be of any location) because it stores meta data in that location which may be needed for compliance reasons.

write and delete operations are not allowed when moving a resource from one resource group to another. That resource can still be read/accessed.

[This page shows whether a resource can be moved or not](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-support-resources)

for ex if you move a VM to another group you will need to move its dependent resources to like database, gateway etc.

<img src="/images/azureadmin/limits.png">

You can also monitor/increase/decrease usage limits.

resource groups cannot be nested.

An Azure Resource Manager template precisely defines all the Resource Manager resources in a deployment. Using Resource Manager templates will make your deployments faster and more repeatable. For example, you no longer have to create a VM in the portal, wait for it to finish, and then create the next VM. Resource Manager takes care of the entire deployment for you.

[Resource manager template format](https://docs.microsoft.com/en-us/learn/modules/configure-resources-arm-templates/3-explore-template-schema)

sample template: 

{%highlight text%}
"parameters": {
  "adminUsername": {
    "type": "string",
    "metadata": {
      "description": "Username for the Virtual Machine."
    }
  },
  "adminPassword": {
    "type": "securestring",
    "metadata": {
      "description": "Password for the Virtual Machine."
    }
  }
{%endhighlight%}


Azure quickstart provides pre-built templates from the community.

The azuredeploy.json file defines the resources that will be deployed and The azuredeploy.parameters.json file provides the values the template needs.

If the resource already exists and no change is detected in the properties, no action is taken. If the resource already exists and a property has changed, the resource is updated. If the resource doesn't exist, it's created.

[18 Oct 2021]

# Automate azure tasks 

azure portal doesn't support automation and hence more prone to errors/failures when performing repetitive tasks. 

TIL: powershell can be installed on linux and Macos too. Took me long enough...

## Powershell

Cmdlets are base commands to which you supply arguments to perform tasks. Cmdlets follow a verb-noun naming convention; for example, Get-Process, Format-Table, and Start-Service. There is also a convention for verb choice: "get" to retrieve data, "set" to insert or update data, "format" to format data, "out" to direct output to a destination, and so on.

Cmdlets are shipped in modules. A PowerShell Module is a DLL that includes the code to process each available cmdlet. You load cmdlets into PowerShell by loading the module they are contained in. You can get a list of loaded modules using the Get-Module command.

The "Az" is the module for azure powershell that contains all the commands for azure administration.

Next we create and play around Vms using azure powershell in an exercise. 

In the exercise we basically had to to just copy and paste the given commands but be sure to save these exercises as they are a great way to play around apart from the stuff you have to do in the exercise. Since there was a lot of manual commands we had to input, next we will create a powershell script for deploying and deleting Vms and its related resources(disks, public IP, virtual network, etc)

[19 Oct 2021]

`During this next module I wondered why the extension for powershell scripts was ".ps1" nd not just "ps". I read from a [forum](https://www.vistax64.com/threads/why-ps1-file-extension-for-ps-scripts.212073/) that they intended to work on version2 of powershell and wanted to differentiate between those two using naming scripts like ".ps1" ,".ps2" and so on. in the end they decided not to do that and now this "1" at the end will haunt us forever.`

Next we learn about powershell basics for using in the script.

Variables: can hold any character along with objects. 

{%highlight text%}
$abc=123
$abc="hello"
$abc=Get-Credential
{%endhighlight%}

Loops: powershell has several loops like any other language. basic syntax:

{%highlight text%}
For ($i = 1; $i -lt 3; $i++)
{
    $i
}
{%endhighlight%}

-lt is less than, -eq is equal, -ne is not equal and so on...

and finally parameters. Again this is similar to other languages.

{%highlight text%}
.\setupEnvironment.ps1 5 "East US"

param([int]$size, [string]$location)

{%endhighlight%}

and then call these variables inside the script.

## azure cli

bash like syntax to interact with azure services. 

`az find` is used to find the most popular commands for use cases. for ex `azure find blob` will give recommendations for the word blob. Similarly it can also be used for command groups like `az find "az vm"`. 

Remember that exercise in the fundamentals course where we had to use azure portal to create a wordpress appservice? we are going to do that using the cli in the next exercise. We create a service plan, then create a webapp and then deploy it.

`For now I just follow along the instructions given in the exercise with a few alterations like name and stuff. After I know all this I will be coming back to these exercises to try and make bigger changes and get comfortable with azure`

{%highlight text%}
export RESOURCE_GROUP=learn-abc
export AZURE_REGION=centralus
export AZURE_APP_PLAN=popupappplan-$RANDOM
export AZURE_WEB_APP=popupwebapp-$RANDOM

az group list --output table
az group list --query "[?name == '$RESOURCE_GROUP']"
az appservice plan create --name $AZURE_APP_PLAN --resource-group $RESOURCE_GROUP --location $AZURE_REGION --sku FREE
az appservice plan list --output table

az webapp create --name $AZURE_WEB_APP --resource-group $RESOURCE_GROUP --plan $AZURE_APP_PLAN
az webapp list --output table
curl $AZURE_WEB_APP.azurewebsites.net

az webapp deployment source config --name $AZURE_WEB_APP --resource-group $RESOURCE_GROUP --repo-url "https://github.com/Azure-Samples/php-docs-hello-world" --branch master --manual-integration
curl $AZURE_WEB_APP.azurewebsites.net
{%endhighlight%}

## Azure resource Manager (ARM templates)

JSON Azure Resource Manager templates (ARM templates) allow you to specify your project's infrastructure in a declarative and reusable way.

reminder: declarative is when we just define a goal and then the system decides how to achieve it, imperative is when all the steps of a goal are defined.

`Bicep is a new language for defining your Azure resources. It has a simpler authoring experience than JSON, along with other features that help improve the quality of your infrastructure as code. We recommend that anyone new to infrastructure as code on Azure use Bicep instead of JSON`

Infrastructure as code enables you to describe, through code(JSON), the infrastructure that you need for your application.

advantages of infrastructure as code:

    Consistent configurations
    Improved scalability
    Faster deployments
    Better traceability

ARM templates allow you to declare what you intend to deploy without having to write the sequence of programming commands to create it.

[ARM template structure](https://docs.microsoft.com/en-us/learn/modules/create-azure-resource-manager-template-vs-code/2-explore-template-structure)

ARM templates can be deployed in following ways:

    Deploy a local template.
    Deploy a linked template.
    Deploy in a continuous deployment pipeline.

More on this later...

Commands to deploy an ARM template

{%highlight text%}
az login

az group create \
  --name {name of your resource group} \
  --location "{location}"

templateFile="{provide-the-path-to-the-template-file}"

az deployment group create \
  --name blanktemplate \
  --resource-group myResourceGroup \
  --template-file $templateFile
{%endhighlight%}

To add a resource to your template, you'll need to know the resource provider and its types of resources. For example, to add a storage account resource to your template, you'll need the Microsoft.Storage resource provider. One of the types for this provider is storageAccount. So your resource type will be displayed as Microsoft.Storage/storageAccounts. You can use a [list of resource providers for Azure](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/azure-services-resource-providers) services to find the providers you need.

Example of an ARM template:

{%highlight text%}
{
   "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
   "contentVersion": "1.0.0.1",
   "apiProfile": "",
   "parameters": {},
   "variables": {},
   "functions": [],
   "resources": [
      {
          "type": "Microsoft.Storage/storageAccounts",
          "apiVersion": "2019-06-01",
          "name": "learntemplatestorage123",
          "location": "westus",
          "sku": {
              "name": "Standard_LRS"
          },
          "kind": "StorageV2",
          "properties": {
              "supportsHttpsTrafficOnly": true
          }
      }
   ],
   "outputs": {}
}
{%endhighlight%}

[20 Oct 2021]

{%highlight text%}
az login
az account set --subscription "Concierge Subscription"

az account list \
   --refresh \
   --query "[?contains(name, 'Concierge Subscription')].id" \
   --output table
az account set --subscription {your subscription ID}

az configure --defaults group=learn-f4f653b9-3e0c-47e0-b7f4-abc

templateFile="azuredeploy.json"
today=$(date +"%d-%b-%Y")
DeploymentName="blanktemplate-"$today

az deployment group create \
 --name $DeploymentName \
 --template-file $templateFile --parameters storageName=\<your parameter\>
{%endhighlight%}

all the deployments that we make using this method are visible for further inspection on the azure portal. Here is how the final template looked like for me after the two exercises.
The purpose of the template was to create storage accounts. We created a template and found that we will need to make changes to it every time we had to deploy a slightly different account so we parameterized it and then we were able to give the changed argument from the command line only. 

Next we changed it so that it would give us some output when the deployment was successful. in this case we made it spit out the URLs of the thus deployed public storage.
{%highlight text%}
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {"storageName": {
        "type": "string",
        "minLength": 3,
        "maxLength": 24,
        "metadata": {
            "description": "Name of azure storage resource"
        }
    }, //comment!
    /*Multi line 
            comment!*/
    "storageSKU": {
   "type": "string",
   "defaultValue": "Standard_LRS",
   "allowedValues": [
     "Standard_LRS",
     "Standard_GRS",
     "Standard_RAGRS",
     "Standard_ZRS",
     "Premium_LRS",
     "Premium_ZRS",
     "Standard_GZRS",
     "Standard_RAGZRS"
   ]
 }},
    "functions": [],
    "variables": {},
    "resources": [{
        "name": "[parameters('storageName')]",
        "type": "Microsoft.Storage/storageAccounts",
        "apiVersion": "2021-04-01",
        "tags": {
            "displayName": "[parameters('storageName')]"
        },
        "location": "[resourceGroup().location]",
        "kind": "StorageV2",
        "sku": {
            "name": "[parameters('storageSKU')]"
        }
    }],
    "outputs": {"storageEndpoint": {
        "type": "object",
        "value": "[reference(parameters('storageName')).primaryEndpoints]"
    }}
}
{%endhighlight%}

I recommend read [this](https://docs.microsoft.com/en-us/learn/modules/create-azure-resource-manager-template-vs-code/3-exercise-create-and-deploy-template),[this](https://docs.microsoft.com/en-us/learn/modules/create-azure-resource-manager-template-vs-code/4-add-flexibility-arm-template) and [this](https://docs.microsoft.com/en-us/learn/modules/create-azure-resource-manager-template-vs-code/5-exercise-parameters-output) for a full understanding of templates since just noting everything down would (in my opinion) not be great note taking practice.

# Manage identities and governance in Azure

Transitioning workloads to the cloud involves more than just moving servers, websites, and data. Companies need to think about how to secure those resources and identify authorized users.

<img src="/images/azureadmin/ad.png">

Azure Active Directory (Azure AD) is Microsoft’s multi-tenant cloud-based directory and identity management service.

Benefits and features:
- Single sign-on to any cloud or on-premises web app such as O365, salesforce, docusign etc.
- Works with iOS, macOS, Android, and Windows devices
- Access your on-premises web applications from everywhere and protect with multi-factor authentication, conditional access policies, and group-based access management
- easy integration of on-premises AD with cloud
- enhance application access security with unique identity protection capabilities. This includes a consolidated view into suspicious sign-in activities and potential vulnerabilities.
- Providing self-service application access and password management through verification steps can reduce help desk calls and enhance security.

Microsoft 365, Azure, or Dynamics CRM Online customer, already use Azure AD. Every Microsoft 365, Azure and Dynamics CRM tenant is already an Azure AD tenant.

## Azure Active Directory 

Azure AD concepts

- Identity. An object that can get authenticated. An identity can be a user with a username and password. Identities also include applications or other servers that might require authentication through secret keys or certificates.
- Account. An identity that has data associated with it. You can't have an account without an identity.
- Azure AD Account. An identity created through Azure AD or another Microsoft cloud service, such as Microsoft 365. Identities are stored in Azure AD and accessible to your organization's cloud service subscriptions. This account is also sometimes called a Work or school account.
- Azure subscription. Used to pay for Azure cloud services.
- Azure tenant/directory. A dedicated and trusted instance of Azure AD, a Tenant is automatically created when your organization signs up for a Microsoft cloud service subscription.

    More instances of Azure AD can be created.
    Azure AD is the underlying product providing the identity service.
    The term Tenant means a single instance of Azure AD representing a single organization.
    The terms Tenant and Directory are often used interchangeably.

## Active Directory Domain Services and Azure Active Directory

AD DS is the traditional deployment of Windows Server-based Active Directory on a physical or virtual server. Apart from AD DS there are other services too in a common AD environment like Active Directory Certificate Services, Active Directory Lightweight Directory Services, Active Directory Federation Services,Active Directory Rights Management Services etc. 

- Azure AD is more internet base (HTTPS and HTTP) rather than LDAP.
- It doesn't use kerberos for authentication and uses HTTP and HTTPS protocols such as SAML, WS-Federation, and OpenID Connect for authentication (and OAuth for authorization).
- USe Federation services(Active Directory Federation Services (ADFS) is a Single Sign-On (SSO) solution created by Microsoft) and other third party services like facebook.
- No OUs(organizational units) or Group object Policies.

[Azure Active Directory PLans](https://docs.microsoft.com/en-us/learn/modules/configure-azure-active-directory/5-select-editions)

## Azure Active Directory Join

Azure AD Join is designed to provide access to organizational apps and resources and to simplify Windows deployments of work-owned devices. Devices can be connected to Azure AD by either registering or joining:


    Registering a device to Azure AD enables you to manage a device’s identity. Azure AD device registration provides the device with an identity that is used to authenticate the device when a user signs-in to Azure AD. You can use the identity to enable or disable a device.

    Joining a device is an extension to registering a device. Joining provides the benefits of registering and changes the local state of a device. Changing the local state enables your users to sign-in to a device using an organizational work or school account instead of a personal account.

## Self service password reset

Enabling Self-service Password Reset (SSPR) gives the users the ability to bypass the help-desk and reset their own passwords.

We can test the SSPR functionality on a selected group and then deploy it to the whole organization(tenant). At least one authentication method is required for reset password. It can be email notification, a text, or code sent to user’s mobile or office phone, or a set of security questions.

security questions are weak. It can be guessed and all the attacker needs is to find its answer.

## configure user and group accounts

There are 3 types of uses in azure ad:

- cloud identities: administrator accounts and users that you manage yourself. Cloud identities can be in Azure Active Directory or an external Azure Active Directory
- directory-synchronized identities: identities present in the on-premises AD that are sync(ed) with the azure ad
- guest users: users existing outside azure. ex: accounts from other cloud providers and Microsoft accounts such as an Xbox LIVE account.

New users can be created using the azure portal.

<img src="/images/azureadmin/newuser.png">

deleted users can be restored within 30 days and you must be a global admin to make these changes.

## bulk management of identities

<img src="/images/azureadmin/bulk.png">

Azure supports bulk creation/deletion of accounts.This can be done via powershell or the portal. Just download the template, fill it up and upload it to azure and bulk users will be created. 

Decide a naming convention before hand. like firstname.lastname@comp.org

## Groups

There are 2 types of groups in azure AD:
- security groups: Security groups are used to manage member and computer access to shared resources for a group of users.
- microsoft 365 groups: Microsoft 365 groups provide collaboration opportunities by giving members access to a shared mailbox, calendar, files, SharePoint site, and more. You can give people outside of your organization access to the group.

ways to assign access rights:
- assigned: Lets you add specific users to be members of this group and to have unique permissions.
- dynamic user: Lets you use dynamic membership rules to automatically add and remove members. When a member's attributes change, azure checks the rules and accordingly adds/removes users to group.
- dynamic device: Lets you use dynamic group rules to automatically add and remove devices. same thing as dynamic users but for devices.

## administrative units

restrict administrative scope by using administrative units in organizations that are made up of independent divisions of any kind. Basically assign administrative access to admins over only azure ad users in one particular division/category/unit.

We can say that its like giving admin powers to users but only over a particular scope. ex: Consider the example of a large university that's made up of many autonomous schools (School of Business, School of Engineering, and so on). Each school has a team of IT admins who control access, manage users, and set policies for their school.

the central admin could give admin powers to the IT admins of their respective school over the students/members of that school.

## configure subscriptions

**region**

In Azure,a region is a geographical area on the planet containing at least one, but potentially multiple datacenters. The datacenters are in close proximity and networked together with a low-latency network.

[azure regions](https://azure.microsoft.com/global-infrastructure/regions/)

billing is done on per-subscription basis.

<img src="/images/azureadmin/subs.png">

Subscriptions contain accounts, which are just a form of identify. There are several ways to get an Azure subscription: Enterprise agreements, Microsoft resellers (provides a simple, flexible way to purchase cloud services from your Microsoft reseller), Microsoft partners , and a personal free account.

Cost Management shows organizational cost and usage patterns with advanced analytics.

The ways that Cost Management help you plan for and control your costs include: Cost analysis, budgets, recommendations, and exporting cost management data. 

Use tags like production,testing etc for better cost management. tags are not inherited by resources of a resource group.

Cost savings in azure:
- Reservations help you save money by paying ahead. 
- Azure Hybrid Benefits is a pricing benefit for customers who have licenses with Software Assurance. Azure Hybrid Benefits helps maximize the value of existing on-premises Windows Server or SQL Server license investments when migrating to Azure.
- Azure Credits is monthly credit benefit that allows you to experiment with, develop, and test new solutions on Azure
- Azure regions pricing can vary from one region to another

## Configuring azure policies

You organize subscriptions into containers called management groups and apply your governance conditions to the management groups. management groups help in custom grouping, applying policies and budgets across subscriptions/accounts.

Each group is assigned a unique group ID and can be given custom group names.

Policies are kind of rules that you define which are checked against all your resources/groups.  Helps in real time policy enforcing and remediation at scale.

Use cases:


    Specify the resource types that your organization can deploy.
    Specify a set of virtual machine SKUs that your organization can deploy.
    Restrict the locations your organization can specify when deploying resources.
    Enforce a required tag and its value.
    Audit if Azure Backup service is enabled for all Virtual machines.

Policies can be created in following steps:
- create definition: define the conditions and what action to take. There are built in definitions to chose from (as well as from [github](https://github.com/Azure/azure-policy/tree/master/samples))but you can also create yours too.
- create initiative definition: what is the purpose of the policy. this will consist of a bunch of policies for that purpose.
- scope the policy: define the scope on which the policy will be checked against (resource group/resource/subscription)
- view results: view how many resources are compliant with your policies. (evaluation occurs every hour)

<img src="/images/azureadmin/policy.png">

<img src="/images/azureadmin/ini.png">


[21 Oct 2021]

## Configuring Role based access control

Role-based access control (RBAC) helps you manage who has access to Azure resources, what they can do with those resources, and what areas they have access to.

Concepts in RBAC:
- security principle: the object that is requesting access to a resource. for ex: user, group, service principle, etc.
- role definition: user, reader, owner, administrator
- scope: resource group, subscription, resource, management group
- assignment: Attaching a role definition to a security principal at a particular scope. basically the process of applying RBAC

Least privilege model should be followed when performing RBAC.

## Role creation

Each role is defined inside a JSON file. It includes name,id,role description,permissions and scope.

<img src="/images/azureadmin/role.png">

Example of role definition:

{%highlight text%}
`Name: Owner
ID: 8e3af657-a8ff-443c-a75c-2fe8c4bcb65
IsCustom: False
Description: Manage everything, including access to resources
Actions: {*}
NotActions: {}
AssignableScopes: {/}
{%endhighlight%}

<img src="/images/azureadmin/def.png">

The image above describes various roles. And below is an example of scoping:

`* /subscriptions/[subscription id]` : scope is the entire subscription
`* /subscriptions/[subscription id]/resourceGroups/[resource group name]` : scope is that resource group
`* /subscriptions/[subscription id]/resourceGroups/[resource group name]/[resource]` : scope is that particular resource

Differences between RBAC roles and roles in Azure Active directory

<img src="/images/azureadmin/roles.png">

types of roles:
- owner: has full access
- contributor: can perform managing tasks but not administrative tasks
- reader: read access only
- User Access Administrator. Lets you manage user access to Azure resources, rather than to managing resources. kinda like opposite of contributor

If these roles aren't enough custom roles can be defined.

[22 Oct 2021]
## Users and groups in Azure AD

