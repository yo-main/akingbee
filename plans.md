# Strategic Feature Recommendations for Akingbee

## Context
- **Current user**: Single hobbyist beekeeper (1-5 hives)
- **Target users**: Semi-pro and professional beekeepers (6-50+ hives)
- **Priorities**: Operational efficiency & better data insights

## Top Priority Features (Ordered by Impact)

### 1. Harvest Analytics Dashboard (HIGHEST PRIORITY)
**Why**: This directly addresses "better data insights" and is critical for semi-pro/pro users who make business decisions based on yield data.

**Current gap**: Harvest data is collected but not analyzed. No visualization, trend analysis, or productivity metrics.

**Recommended features**:
- **Harvest trends over time**: Line charts showing total honey production by month/season/year
- **Hive productivity comparison**: Bar charts comparing yield per hive
- **Apiary-level analytics**: Total production per apiary, average yield per hive
- **Year-over-year comparison**: Compare current year harvest to historical data
- **Export to CSV**: For external analysis and record-keeping

**Why this matters for target users**:
- Hobbyists: Understand which hives are healthy and productive
- Semi-pro/Pro: Make data-driven decisions about which queens/genetics to propagate, which apiaries are most profitable

**Implementation approach**:
- Add analytics page/section accessible from main navigation
- Use Chart.js or similar lightweight charting library (HTMX-compatible)
- Create new repository methods to aggregate harvest data by time periods
- Add CSV export endpoint for harvest data

**Estimated complexity**: Medium (1-2 weeks)

---

### 2. Task Scheduling & Reminders (HIGH PRIORITY)
**Why**: Addresses "operational efficiency" - beekeeping is time-sensitive (treatments must be applied at specific intervals, feeding schedules, inspection routines).

**Current gap**: No way to schedule future tasks or get reminders for time-sensitive operations.

**Recommended features**:
- **Task creation**: Add tasks with due dates, priorities, and hive/apiary associations
- **Task list view**: See upcoming tasks sorted by date
- **Task completion tracking**: Mark tasks done with notes/outcomes
- **Optional email reminders**: Daily digest of upcoming tasks (important for semi-pro/pro)
- **Recurring tasks**: Weekly inspections, monthly treatments

**Why this matters for target users**:
- Hobbyists: Won't forget critical feeding or treatment dates
- Semi-pro/Pro: Manage complex schedules across multiple apiaries, delegate tasks to helpers

**Implementation approach**:
- New `TASK` table with due_date, priority, status, recurrence rules
- Task API endpoints (CRUD operations)
- Task list page (similar to existing hive/apiary pages)
- Simple email notification service (optional, can use SMTP)
- Integration with existing journal/comment system

**Estimated complexity**: Medium-High (2-3 weeks with email notifications)

---

### 3. Quick Stats Dashboard (MEDIUM-HIGH PRIORITY)
**Why**: Addresses "better data insights" with at-a-glance operational metrics.

**Current gap**: No summary view of key metrics across all hives/apiaries.

**Recommended features**:
- **Total hive count** (active, queenless, concerning health)
- **This season's total harvest** with comparison to last year
- **Upcoming tasks count** (once task system implemented)
- **Recent activity feed** (last 7 days of comments/harvests)
- **Health status overview**: Count of hives by swarm health

**Why this matters for target users**:
- Hobbyists: Quick check-in without drilling into individual hives
- Semi-pro/Pro: Executive summary for decision-making

**Implementation approach**:
- Enhance existing `/overview` page or create new `/dashboard` route
- Add repository methods for aggregate queries (count hives by health, sum harvests by date range)
- Display as cards/widgets on main page
- Lightweight - mostly database aggregation queries

**Estimated complexity**: Low-Medium (1 week)

---

### 4. Mobile-Responsive Design (HIGH PRIORITY for future growth)
**Why**: Professional beekeepers need field access on phones/tablets. Current hobbyist may not need it, but semi-pro/pro absolutely will.

**Current gap**: No indication of responsive design or mobile optimization.

**Recommended features**:
- Responsive CSS for all existing pages
- Touch-friendly form inputs
- Simplified mobile navigation (hamburger menu)
- Field-optimized quick-add forms (minimal fields, defaults to today's date)

**Why this matters for target users**:
- Hobbyists: Nice to have
- Semi-pro/Pro: Essential - they're at apiaries in the field and need to log observations immediately

**Implementation approach**:
- Add responsive CSS framework or custom media queries
- Test all existing pages on mobile viewports
- Optimize forms for mobile (larger touch targets, date defaults)
- Consider PWA manifest for "add to home screen"

**Estimated complexity**: Medium (1-2 weeks depending on current CSS structure)

---

### 5. Apiary-Level Comments & Observations (MEDIUM PRIORITY)
**Why**: Addresses "operational efficiency" - sometimes observations apply to entire apiary (weather, forage availability, bears/pests).

**Current gap**: Comments can only be on individual hives. No apiary-level notes visible on apiary list.

**Recommended features**:
- Add comment section to apiary detail page (similar to hive detail)
- Show most recent apiary comment on apiary cards in overview
- Filter comments by type (note/action/forage/weather)

**Why this matters for target users**:
- Hobbyists: Track location-specific conditions
- Semi-pro/Pro: Understand why entire apiaries perform differently (forage, microclimate)

**Implementation approach**:
- Extend existing comment system (already supports apiary_id foreign key)
- Add apiary detail page with comment section
- Update overview page to show apiary comments

**Estimated complexity**: Low (3-5 days) - leverages existing comment infrastructure

---

## Secondary Features (Nice to Have)

### 6. Hive Health Trend Tracking
- Track swarm health changes over time
- Alert when hive health degrades
- Useful for: Semi-pro/pro users managing many hives

### 7. Treatment/Medication Tracking
- Record treatments applied (type, dosage, date)
- Track withdrawal periods before harvest
- Critical for: Semi-pro/pro selling honey commercially (regulatory compliance)

### 8. Equipment Inventory
- Track supers, frames, feeders
- Know what equipment is at which apiary
- Useful for: Semi-pro/pro managing multiple apiaries

### 9. Weather Integration
- Fetch local weather data
- Correlate weather with hive activity/harvests
- Useful for: All users for planning inspections

### 10. Multi-User Collaboration
- Share apiary access with partners/helpers
- Role-based permissions (viewer/editor)
- Useful for: Semi-pro/pro with employees, hobbyist teaching family

---

## Recommended Implementation Order

**Phase 1: Data Insights Foundation** (4-6 weeks)
1. Quick stats dashboard (1 week)
2. Harvest analytics with charts (2 weeks)
3. CSV export functionality (3-5 days)

**Phase 2: Operational Efficiency** (4-6 weeks)
4. Task scheduling system (2-3 weeks)
5. Apiary-level comments enhancement (3-5 days)
6. Email reminders for tasks (1 week)

**Phase 3: Professional Polish** (2-4 weeks)
7. Mobile-responsive design (1-2 weeks)
8. User profile/settings page (3-5 days)
9. Performance optimization (ongoing)

**Phase 4: Advanced Features** (as needed)
10. Treatment tracking
11. Equipment inventory
12. Weather integration
13. Multi-user collaboration

---

## Key Technical Considerations

### For Harvest Analytics
- Use lightweight charting library compatible with HTMX (Chart.js, ApexCharts)
- Create new repository aggregate methods
- Consider caching for performance with large datasets

### For Task System
- Simple SMTP email service for reminders (golang.org/x/smtp or gomail)
- Cron job or scheduled worker for reminder checks
- Keep UI consistent with existing journal/comment patterns

### For Mobile Responsiveness
- Audit existing CSS structure
- Add Tailwind or custom responsive breakpoints
- Test on actual devices, not just browser dev tools

### For All Features
- Maintain existing architecture patterns (domain/service/repository)
- Keep HTMX-first approach for consistency
- Add comprehensive tests for new features
- Update migrations incrementally

---

## Why This Prioritization?

1. **Harvest analytics first** because it provides immediate value to current user while being a differentiator for attracting semi-pro users
2. **Task scheduling next** because operational efficiency was stated priority and this prevents costly mistakes (missed treatments)
3. **Mobile responsiveness** is essential before marketing to semi-pro/pro users but can wait until core features are solid
4. **Secondary features** are valuable but not blocking for target audience adoption

This approach delivers value incrementally while building toward a professional-grade beekeeping management platform.
