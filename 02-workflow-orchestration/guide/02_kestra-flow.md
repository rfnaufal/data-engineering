## Kestra

### Concept

Before building any workflows, let’s briefly understand how Kestra organizes automation.

In Kestra, everything is built around the idea of **flows**.

A flow represents an end-to-end workflow composed of:

- tasks — what gets executed
- triggers — when it runs
- dependencies — execution order and conditions
- inputs — parameters passed into the flow
- outputs — data produced and shared between tasks

Once you understand flows, creating orchestration becomes much easier.

---

### Creating Workflows (Flows)

Now that we understand the core concept, let’s create our first workflow.

In this module, we’ll start by uploading a provided workflow directly in the Kestra UI.  
This is the fastest way to explore how flows work visually.

Later on, we’ll also create workflows programmatically by sending POST requests to Kestra’s API, which is more suitable for real production and automation.

---

### Exploring the Hello-World Flow

The [`01_hello_world.yaml`](https://github.com/rfnaufal/data-engineering/blob/main/02-workflow-orchestration/flows/01_hello_world.yaml) flow brings all of these concepts together in these example.

Here’s what this workflow includes:

- Five tasks in total: three log tasks and one sleep task  
- An input called `name`  
- A variable that uses the `name` input to generate a full welcome message  
- An output created from the return task and logged in a later log task  
- A trigger that runs the flow every day at 10 AM  
- Plugin defaults that send all log messages at the `ERROR` level  
- A concurrency limit of two executions — any additional runs while two are active will fail

Note:

Once a flow is created, its namespace and id CANNOT be changed.