from typing import Any, Dict, List

from .base import AgentConfig, BaseAgent


class StakeholderNotifierAgent(BaseAgent):
    """Agent responsible for notifying stakeholders about flight delays."""

    def __init__(self):
        config = AgentConfig(
            name="StakeholderNotifier",
            role="Communications Specialist",
            goal="Efficiently notify all relevant stakeholders about flight delays and changes to plans",
            backstory="""You are a communications expert who excels at crafting clear, concise messages
            tailored to different audiences. You understand the importance of providing timely updates
            and can prioritize notifications based on urgency and recipient needs.""",
            verbose=True,
            allow_delegation=False,
        )
        super().__init__(config)

    async def notify_stakeholders(
        self,
        calendar_event: Dict[str, Any],
        contacts: List[Dict[str, Any]],
        updated_eta: str,
        delay_reason: str = "Unknown",
    ) -> Dict[str, Any]:
        """Notify stakeholders about flight delays and updated arrival times."""
        task = f"""Create and send notifications to all stakeholders about flight delay:

        Event details:
        - Event: {calendar_event.get("title")}
        - Original time: {calendar_event.get("original_time")}
        - Location: {calendar_event.get("location")}

        Delay details:
        - Updated ETA: {updated_eta}
        - Reason for delay: {delay_reason}

        Stakeholders to notify:
        {self._format_contacts(contacts)}

        Tasks:
        1. Craft appropriate messages for each stakeholder category (meeting attendees, hosts, etc.)
        2. Prioritize notifications based on urgency and impact
        3. Suggest appropriate communication channels for each stakeholder (email, SMS, etc.)
        4. Draft follow-up communications if needed

        Provide the notification plan and message drafts for each stakeholder group."""

        context = {
            "calendar_event": calendar_event,
            "contacts": contacts,
            "updated_eta": updated_eta,
            "delay_reason": delay_reason,
        }

        return await self.execute(task, context)

    def _format_contacts(self, contacts: List[Dict[str, Any]]) -> str:
        """Format the contacts list for the task prompt."""
        formatted = ""
        for i, contact in enumerate(contacts):
            formatted += f"- Contact {i + 1}: {contact.get('name')} ({contact.get('role')}), "
            formatted += f"Preferred contact: {contact.get('preferred_contact', 'Email')}\n"
        return formatted
