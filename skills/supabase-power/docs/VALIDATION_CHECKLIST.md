# Skill Validation Checklist

Before publishing, verify:

## Structure
- [ ] SKILL.md exists with proper YAML frontmatter
- [ ] README.md has installation instructions
- [ ] All four pattern templates exist in templates/
- [ ] Policy library exists in policies/
- [ ] At least one example exists in examples/

## Content
- [ ] SKILL.md clearly explains when to use the skill
- [ ] Each template has AskUserQuestion examples
- [ ] Policy library has SQL code blocks
- [ ] Examples show complete migrations

## Functionality
- [ ] Test single-user pattern workflow manually
- [ ] Verify migration SQL syntax is valid
- [ ] Check that RLS policies are properly commented
- [ ] Confirm validation tests are specific and runnable

## Documentation
- [ ] README has clear installation steps
- [ ] Examples show realistic use cases
- [ ] Policy library explains gotchas
- [ ] Templates explain when to use each pattern
