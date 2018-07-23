
**Cloud Custodian:**
  Cloud Custodian an is open source project from CapitalOne.
  It is a rules engines for AWS fleet management. It allows users to define policies
  to enable a well managed cloud infrastructure.

  Cloud Custodian can be used to manage AWS accounts by ensuring real time compliance
  to security policies (IAM policies, SecurtyGroups etc), tag policies and cost
  management.

  For more information [Cloud Custodian github](https://github.com/capitalone/cloud-custodian)

  For documentation [Documents](http://www.capitalone.io/cloud-custodian/docs/)

**cloud_custodian.yaml:**

  CloudFormation template for setting up an Amazon Linux Cloud Custodian server.

**Custodian_policy.yml:**

  Custodian policy file. Current policies only send email
  when an AWS resource fails compliance test. Policies can be created for taking actions
  on resource (stop, terminate, remove) when resource fails compliance.

  [EC2 example](http://www.capitalone.io/cloud-custodian/docs/usecases/amicomp.html)

  [S3 example](http://www.capitalone.io/cloud-custodian/docs/usecases/s3globalgrants.html)

  [Tag compliance](http://www.capitalone.io/cloud-custodian/docs/usecases/tagcompliance.html)

**Quick Install:**

  Create a CloudFormation stack using cloud_custodian.yaml

  Copy custodian_policy.yml file to /opt/custodian_policies/ in custodian server (use Jenkins for this?)

  Run
  ```
  /opt/cloud-custodian/tools/c7n_mailer/bin/custodian run -s .
  /opt/custodian_policies/custodian_policy.yml --region us-west-2 --cache 0
  ```

**Current Setup:**

 CloudFormation template create an Amazon linux server, download
 custodian, create SQS queue for sending message when custodian a resource that
 fails the check, create an install script for installing c7n_mailer lambda which is used
 for sending alert e-mails.

**Email Message Relay:**

  Custodian mailer lambda function susbscribe to an SQS
  queue, lookup users, and send email via SES.
  Custodian mailer [Documents](https://github.com/capitalone/cloud-custodian/tree/master/tools/c7n_mailer)

**To Do:**

  The above command can be run in a cron schedule for periodically checking resource compliance.

  A wrapper script can be created for monitoring more than one AWS account.
  When monitoring more than one account, ensure that you create a cross account role
  for custodian.

  **Current workflow:**

  Custodian_Check_for_Violation --> Send_message_to_SQS --> Mailer_Lambda_Check_SQS --> Send_Email_via_SES
