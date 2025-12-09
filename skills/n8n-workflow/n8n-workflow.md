---
description: Build n8n workflows via MCP for Held Lab & Reconnect Academy. Covers Zoho Mail OAuth2, AI email classification, and frontend webhook integrations.
---

# n8n Workflow Automation Skill

Build and manage n8n workflows directly from Claude Code using the n8n-mcp server.

## Environment

| Property | Value |
|----------|-------|
| n8n Instance | `https://n8n.heldlab.be` |
| MCP Server | `n8n-mcp` |
| Primary Brand | Held Lab (biohacking, recovery) |
| Secondary Brand | Reconnect Academy (MMA/BJJ) |

---

## Step 1: Verify MCP Connection

Before building workflows, verify the n8n-mcp connection:

```
# Check available n8n MCP tools
mcp__n8n__* tools should be available
```

**Common MCP operations:**
- `mcp__n8n__list_workflows` - List all workflows
- `mcp__n8n__get_workflow` - Get workflow details
- `mcp__n8n__create_workflow` - Create new workflow
- `mcp__n8n__update_workflow` - Update existing workflow
- `mcp__n8n__execute_workflow` - Trigger workflow execution
- `mcp__n8n__get_executions` - View execution history

---

## Step 2: Identify Workflow Type

**Ask the user which type of workflow they need:**

| Type | Template | Use Case |
|------|----------|----------|
| Email Triage | `email-classification.md` | AI-powered email sorting |
| Zoho Integration | `zoho-mail-oauth.md` | OAuth2 mail setup |
| Webhook Handler | `webhook-patterns.md` | Frontend form submissions |
| Custom | - | Build from scratch |

**Load the relevant template from:** `templates/[template-name].md`

---

## Step 3: Workflow Design Principles

### Naming Convention
```
[brand]-[function]-[trigger]
```
**Examples:**
- `held-email-triage-schedule`
- `reconnect-lead-webhook`
- `held-booking-confirmation-trigger`

### Error Handling Pattern
Always include:
1. **Error Trigger node** - Catch workflow failures
2. **Notification node** - Alert on critical errors (Slack/Email)
3. **Logging** - Store execution data for debugging

### Node Organization
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Trigger   │───▶│  Process    │───▶│   Action    │
│  (webhook/  │    │  (filter/   │    │  (send/     │
│   schedule) │    │   transform)│    │   store)    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Error     │
                   │   Handler   │
                   └─────────────┘
```

---

## Step 4: Integration Credentials

### Zoho Mail (OAuth2)
See: `templates/zoho-mail-oauth.md`

### Supabase
```json
{
  "host": "https://[project-id].supabase.co",
  "serviceRoleKey": "{{$credentials.supabaseServiceKey}}"
}
```

### OpenAI / Claude
```json
{
  "apiKey": "{{$credentials.openaiApiKey}}"
}
```

---

## Step 5: Testing & Deployment

### Test Checklist
- [ ] Trigger fires correctly (manual test)
- [ ] Data transformation produces expected output
- [ ] Error handling catches failures
- [ ] Credentials work in production
- [ ] Webhook URLs are secured (if applicable)

### Activation
```
1. Test workflow with sample data
2. Review execution logs
3. Activate workflow
4. Monitor first real executions
```

---

## Quick Reference

| Resource | Link |
|----------|------|
| n8n Instance | https://n8n.heldlab.be |
| n8n Docs | https://docs.n8n.io |
| Zoho API Console | https://api-console.zoho.eu |
| Webhook Security | See `webhook-patterns.md` |

---

## Health/Fitness Workflow Ideas

### Held Lab
- Email triage (spam, klant, aanvraag, dienst-vraag)
- Booking confirmations
- Follow-up sequences
- Review requests post-treatment

### Reconnect Academy
- Trial class follow-ups
- Membership renewal reminders
- Class schedule notifications
- Lead nurturing sequences
