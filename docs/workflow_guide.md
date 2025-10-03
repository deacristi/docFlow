## **Phase 1: Root Cause Investigation**
1. **Context Health Check**: Run `python scripts/context_dashboard.py` to verify AI context is healthy before starting investigation. If accuracy < 90% or usage > 70%, refresh context first.
2. **Thorough Analysis**: Use codebase-retrieval tools to examine each file containing `async with get_db_session()` patterns. Verify these are actual runtime errors, not just pattern differences.
3. **Context Refresh**: Review `@f:\Docs\Dev\AI Scripts\TradePulse\TradePulse_final_augment\backend_v4/docs\initial_prompt.md` to understand TradePulse v4.0 architecture, development standards, and current implementation status.
4. **MCP Tool Utilization**: Leverage available MCP tools (filesystem, database, GitHub, Microsoft docs, browser automation) to gather comprehensive information about the affected files and their usage patterns.
5. **100% Certainty Requirement**: Do not proceed until you have absolute certainty about the root cause and can demonstrate the actual failure these patterns cause.

## **Phase 2: Documentation**

**Issue Analysis Document**: Create a comprehensive root cause analysis using the template `@f:\Docs\Dev\AI Scripts\TradePulse\TradePulse_final_augment\backend_v4/docs\issues\issue_root_cause_analysis_template.md`. Save the new document in `@f:\Docs\Dev\AI Scripts\TradePulse\TradePulse_final_augment\backend_v4/docs\issues/` with a descriptive filename.

## **Phase 3: Solution Design**

**Standards Compliance**: Analyze `@f:\Docs\Dev\AI Scripts\TradePulse\TradePulse_final_augment\backend_v4/docs\development_standards.md` to ensure your solution follows established patterns and constraints.

**Conservative Solution**: Design a fix that is guaranteed to resolve the issue without impacting existing functionality or code integrity. Prioritize minimal, surgical changes over comprehensive rewrites.

## **Phase 4: Implementation Planning**

**Implementation Plan**: Create a detailed implementation plan using `@f:\Docs\Dev\AI Scripts\TradePulse\TradePulse_final_augment\backend_v4/docs\implementation_plans\implementation_plan_template.md` that includes testing strategy, rollback procedures, and verification steps.

## **Phase 5: Code Implementation**

**Code Development**: Write the necessary code changes to resolve the issue while adhering to the implementation plan and development standards.

**Testing**: Implement unit tests, integration tests, and performance benchmarks to validate the solution.

**Use virtual environment**: All testing and validation must be done within the virtual environment (venv) to ensure consistency and accuracy.

**Documentation**: Update relevant documentation, including API references and user guides, to reflect any changes made.

## **Phase 6: Code Review & Validation**

**Code Review**: Act as the development team and review the code changes. Address any feedback and iterate until all concerns are resolved.

**Validation**: Perform a final round of testing and validation to ensure the solution meets all requirements and quality standards.


**Quality Standards**: 
- Only proceed if the issues cause actual runtime failures
- Write production-grade code that adds real value to TradePulse
- Ensure all changes are backward compatible and maintain system stability
- Test thoroughly using the virtual environment (venv) before declaring success