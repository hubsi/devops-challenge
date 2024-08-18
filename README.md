# devops-challenge
Limehome Devops Challenge

## s3 text file search script
Searches for files in the specified S3 bucket that contain a given substring (case-insensitive).
Handles potential encoding issues by attempting different decoding strategies.

Args:
- bucket_name: Name of the S3 bucket to search.
- search_string: Substring to search for in the files (case-insensitive).

Returns:
- List of file names containing the substring.

### setup

#### create venv
It is recommended to use python venv to avoid dependency conflicts:

    python3 -m venv .venv
    source .venv/bin/activate

#### install dependencies

    python3 -m pip install -r requirements.txt

#### configure AWS credentials

You'll need to configure aws credentials with access to the s3 bucket. e.g. using `aws configure` or exporting the AWS_PROFILE env var for the desired profile. If the aws cli can list the contents of the bucket with the active profile, this script should work. You can test with: `aws s3 ls s3://s3_bucket_name/`

### usage

    python s3filesearch.py <s3_bucket_name> <substring>

#### running unit tests

    python3 -m unittest test_s3filesearch.py

### limitation / improvements
- The current version only supports text formats. Decoding of .docx and .pdf or other file types would have to be added if necessary
- The application can be containerized with a Dockerfile to skip pyenv setup and requirements installation.


## Concepts
Please explain the following concepts in your own words. Assume that we know nothing about them.
### Infrastructure as Code
What is it? Why would I want it? Are there any alternatives ?

Infrastructure as Code is the state of the art for managing and provisioning computer infrastructure, using code to decribe the infrastructure allowing reproducible automated deployments. The term infrastructure refers to the components needed to run applications (e.g. servers, networks, databases) and the term code means programming scripts and configuration files that define the infractructure.
Advantages are:
- Consistency: IaC ensures that environments (like development, testing, and production) are consistent. By using the same code to set up each environment, you reduce the chances of errors or inconsistencies.
- Automation: Automating infrastructure setup saves time and reduces the chance of human error, making deployments faster and more reliable.
- Version Control: Since infrastructure is defined in code, it can be stored in version control systems like Git. This allows you to track changes, roll back to previous versions, and collaborate more effectively with others.
- Scalability: IaC makes it easier to scale infrastructure up or down quickly by automating the process of adding or removing resources as needed.
- Reproducibility: You can recreate entire environments quickly by re-running the code, which is useful for disaster recovery, testing, and deploying to new regions. You can also reuse code for similar infrastructure and thus facilitate infrastructure standards and secure defaults.

Before IaC became popular, infrastructure was often managed manually, either through graphical interfaces or by manually executing commands on servers. These methods are error-prone, time-consuming, and hard to replicate across environments, which is why those aren't real alternatives to IaC aside from edge cases where the advantages from IaC aren't very important and/or setup of IaC is higher effort than manual management.


### Observability
Please explain this term in the context of micro services. What do we want to observe? What kind of challenges do you see in a distributed environment? How can we solve them?

Observability in the context of microservices is understanding the behavior of a distributed system by analyzing the data it produces like logs, metrics and traces. We want to observe the performance and reliability of the entire system, health of services, interaction/communication including errors, performance metrics like processing time / latency, resource usage for cpu, memory and network bandwith, and error rates.
Challenges in distributed environments are complexity, high data volume, correlation vs. causation, distributed tracing (following requests through different components/services) and performance overhead/latency from observability agents. To overcome some of them, logging and monitoring should be centralized ideally into a single tool with distributed tracing across services and automated alerts. Collecting only the necessary observability data helps reduce performance overhead and allows focusing on the most critical information. A service mesh can help manage and observe network communication with built in tracing and metrics.

## Security
Imagine you would join our team and put in charge of securing our AWS infrastructure. What are the first three things that you check, to limit the risk of a breach? Explain why.

Some of the most common attacks on AWS infrastructure are Misconfiguration Attacks, Credential Compromise, Account Takeover and Privilege Escalation. A review of the IAM policies enforcing need to know/least privilege, requiring MFA for all users, and checking policies for misconfigutations should therefore be the first step to limit the risk of such attacks. 

Step two would be checking for common weaknesses/mistakes outside IAM policies that are relatively easy to remediate like leaked credentials (e.g. in code repositories - use git-secrets) or public s3 buckets. 

Reviewing the AWS account structure as step three will also reduce the risk of a breach, since the impact for a single compromised account or role is reduced when other accounts are not affected. This particularly includes the usage of organization accounts and logging/monitoring/audit accounts and separation of sandbox/dev/test/production accounts. By evaluating the AWS account structure, you can ensure that your organization is not only secure but also scalable and manageable. This approach helps maintain a clear separation of concerns, improves the implementation of security best practices like centralized logging, and facilitates easier auditing and compliance checks across different environments within the organization. While many other things could be checked in step three and might be easier to remediate/approach, this fundamental step is important to get the full picture of the account structure and associated risks, and resulting changes to the account structure can also break/remediate changes that might have been required due to other security checks (e.g. centralized logging).
