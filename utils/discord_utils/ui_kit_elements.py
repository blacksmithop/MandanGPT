from discord import Interaction, SelectOption, TextStyle
from discord.ui import Modal, Select, TextInput, View
from utils import summarize_text

# Constants for default values
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_P = 0.9
DEFAULT_NUM_CTX = 100


# Feedback Form
class FeedbackForm(Modal, title="Feeedback"):
    feedback = TextInput(
        label="What do you think about this bot?",
        style=TextStyle.long,
        placeholder="Type your answer here...",
        required=True,
        max_length=256,
    )

    async def on_submit(self, interaction: Interaction):
        self.interaction = interaction
        self.answer = str(self.feedback)
        self.stop()


class SummarizeModal(Modal, title="Summarize Text"):
    def __init__(
        self,
        summary_type: str,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
        num_ctx: int = DEFAULT_NUM_CTX,
    ):
        super().__init__()
        self.summary_type = summary_type
        self.temperature = temperature
        self.top_p = top_p
        self.num_ctx = num_ctx

        # Text input for content to summarize
        self.text_input = TextInput(
            label="Text to summarize",
            style=TextStyle.paragraph,
            placeholder="Paste the text you want to summarize here...",
            required=True,
            max_length=4000,
        )
        self.add_item(self.text_input)

        # Parameter inputs with appropriate validation
        self.temp_input = TextInput(
            label="Temperature (0-2, creativity)",
            default=str(temperature),
            required=True,
        )
        self.add_item(self.temp_input)

        self.top_p_input = TextInput(
            label="Top P (0-1, diversity)", default=str(top_p), required=True
        )
        self.add_item(self.top_p_input)

        self.num_ctx_input = TextInput(
            label="Context Length (tokens)", default=str(num_ctx), required=True
        )
        self.add_item(self.num_ctx_input)

    async def on_submit(self, interaction: Interaction):
        try:
            # Validate inputs
            temperature = float(self.temp_input.value)
            top_p = float(self.top_p_input.value)
            num_ctx = int(self.num_ctx_input.value)

            if not 0 <= temperature <= 2:
                raise ValueError("Temperature must be between 0 and 2")
            if not 0 <= top_p <= 1:
                raise ValueError("Top P must be between 0 and 1")
            if num_ctx <= 0:
                raise ValueError("Context length must be positive")

            print(f"{temperature=} {top_p=} {num_ctx=}")
            text_to_summarize = self.text_input.value
            print(f"{text_to_summarize[:100]=}")

            # Call your summarization function
            summary_text, usage_metadata = await summarize_text(
                text=text_to_summarize,
                temperature=temperature,
                top_p=top_p,
                num_ctx=num_ctx,
            )
            print(f"{summary_text[:100]=}")
            print(f"{usage_metadata=}")

            await interaction.response.send_message(
                f"**{self.summary_type.capitalize()} Summary:**\n"
                f"{summary_text}\n\n"
                f"*Parameters used:*\n"
                f"- Temperature: {temperature}\n"
                f"- Top P: {top_p}\n"
                f"- Context Length: {num_ctx}",
                ephemeral=False,
            )

        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}", ephemeral=True
            )


class SummaryTypeView(View):
    def __init__(self):
        super().__init__()

        # Summary type options
        type_options = [
            SelectOption(
                label="Short",
                value="short",
                description="Concise bullet points or 1-2 sentences",
            ),
            SelectOption(
                label="Medium",
                value="medium",
                description="Paragraph summary with key points",
            ),
            SelectOption(
                label="Elaborate",
                value="elaborate",
                description="Detailed summary with examples",
            ),
        ]

        self.select = Select(placeholder="Choose summary type...", options=type_options)
        self.select.callback = self.on_summary_type_select
        self.add_item(self.select)

    async def on_summary_type_select(self, interaction: Interaction):
        summary_type = interaction.data["values"][0]

        # Default parameters based on summary type
        type_params = {
            "short": (0.2, 0.9, DEFAULT_NUM_CTX),  # More focused, less creative
            "medium": (0.2, 0.9, DEFAULT_NUM_CTX * 3),  # Balanced
            "elaborate": (0.5, 0.95, DEFAULT_NUM_CTX * 5),  # More creative/verbose
        }

        temperature, top_p, num_ctx = type_params.get(
            summary_type, (DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_NUM_CTX)
        )

        # Show the parameter customization modal
        await interaction.response.send_modal(
            SummarizeModal(
                summary_type=summary_type,
                temperature=temperature,
                top_p=top_p,
                num_ctx=num_ctx,
            )
        )


async def setup_summarize_command(bot):
    @bot.tree.command(
        name="summarize", description="Summarize text with customizable parameters"
    )
    async def summarize(interaction: Interaction):
        """Command to start the summarization process"""
        view = SummaryTypeView()
        await interaction.response.send_message(
            "📝 First, choose your summary type:", view=view, ephemeral=True
        )
