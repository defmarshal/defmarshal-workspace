# Heartbeat tasks for Def

## Time check
- Check current time and date (show in UTC+7)
- Note if it's late (after 23:00) or early (before 08:00) your time

## Daily checks (2-4 times per day)
- **Weather**: Check Bangkok weather (use weather skill)
- **System**: Check disk space and updates if needed
- **Holiday**: Show the nearest Indonesian holiday (date, day, days from today) from `indonesia-holidays-full-2026.md`

## Proactive notifications
Alert if:
- Weather shows rain/storms in Bangkok
- System needs attention (low disk, updates)
- It's been >8h since last conversation

## Quiet times
- Between 23:00-08:00 your time (unless urgent)
- When you're likely sleeping or busy