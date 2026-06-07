# python-ai-new

Scaffold a new Python repository with harness for AI first engineering.

```bash
python-ai-new <project_name>
```

The command creates a folder named `project_name`, scaffolding it with AI
 harness defined in [template](./template/). It also replaces `{{PROJECT_NAME}}` placeholders in text files with `project_name`.

If you pass in a folder path to the command, the last segment of the path is
taken as `project_name`. If you pass in `.`, the current folder name is taken
as `project_name`. For example:

```bash
cd /path/to/my-target-project
python /this-repo-root/python-ai-new main.py .

# or
cd /this-repo-root/python-ai-new
python-ai-new /path/to/my-target-project
```

After the project is created, go to its root README to get started.
