- what components should we add to this MCP ? (we should suggest this)
- Define the structure and how we plan to deploy this MCP server
- Come up with a doc details the demographic using the skills, what the usual workflow we can infer, what the team level of familiarity with AI, what the highest value skills in the repo ? What current usecases this cover? What 


Baseline:
Team composition: 10 people know how to use Claude Code, 5 peoples haven't use Claude Code before
Target: Non-technical staff, with 1 Technical person to review changes (drawback still need to install claude/git)
Components:
  - common: 
    - tool for setup on new machine, debug setup
    - skill creation workflow and claude memory maintance skills
    - low level data plumbing and small business tasks (MoM, create user, ask questions)
  - tasks: personal GTD/Zettelkasten
    - CLAUDE.md only cover shape no natural language triggers for agents
    - target: PM/AM or report makers for C-level/Managers
    - Use Tasky as source of truth
    - Use Obsidian for hand-annotate/update past-reports 
    - Send report to kintone
  - kintai:
    - automate time logging to internal solution
    - help with bulk approve attendance/leave for managers
    - review monthly overtime
    - work hour trackers for all employees
  - reminder:
    - create reminder for self or people
    - can post to team via playwright
  - video-hightlight
    - Used by technical staff for video production
    - Using ffmped/hyperframe with playwright to generate video of interactions
  - data:
    - user: regional planners, sales managers, account managers
    - ad hoc query, analysis, small update


Problems:
- Require non-tech user to remember commands/skills (lacking signpost)
- No way for non-tech to quickly review output from agent
- No way for automatically collecting feedback of skills
- No prompt and context engineering skills from staff
- No drift detection
- E2E skill no gates
- Two failure mode: over-trusting and reflectively untrusting
- Hidden complexity with Obsidian workflow not explained for new hires





Resource for futher exploration:
- https://arxiv.org/abs/2510.26518 - Anthorpic research paper on human AI oversight 