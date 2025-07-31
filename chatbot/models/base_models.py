from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.hashers import make_password
from simple_history.models import HistoricalRecords
from chatbot.models import LLMProvider, LLMModel, CompanyBotTypeChoices, CompanyBotDynamicContextType, ChatStatus, \
    ProfileType



class Bot(models.Model):

    name = models.CharField(max_length=100, help_text="Enter the name of the bot.")
    context = models.TextField(help_text="Provide the bot's main prompt or description of its purpose.")
    max_token = models.IntegerField(default=2048, validators=[MinValueValidator(1)])

    bot_temperature = models.FloatField(
        default=0,
        help_text="Set the temperature for controlling response randomness (0-1). Lower values produce more "
                  "deterministic responses."
    )
    top_k = models.IntegerField(
        default=2, validators=[MinValueValidator(1)],
        help_text="Set the top-k value for the bot's response selection. This defines how many top options to consider "
                  "for each response."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    provider = models.CharField(
        max_length=100, choices=LLMProvider.choices, default=LLMProvider.OPENAI,
        help_text="Select the LLM provider (BEDROCK, BEDROCK_CONVERSE, or OPENAI)"
    )
    provider_keys = models.TextField(
        default="", max_length=1000, null=False, blank=True,
        help_text="API keys or credentials for the selected LLM provider."
    )
    llm_model = models.CharField(
        max_length=100, choices=LLMModel.choices, default=LLMModel.GPT4_O_MINI,
        help_text="Select the LLM model to be used by the bot (e.g., GPT-4o, GPT-4)."
    )
    filter_score = models.FloatField(
        default=0.8,
        help_text="Set the filter score for bot response selection (0-1). Responses below this score will be "
                  "filtered out."
    )
    end_context = models.TextField(
        null=True, blank=True,
        help_text="Provide additional prompt or context to append at the end of the main prompt to guide the "
                  "conversation"
    )
    introductory_message = models.CharField(
        max_length=1000, null=True, blank=True,
        help_text="Provide an introductory message that the bot will present when the conversation starts."
    )
    abrupt_introductory_message = models.CharField(max_length=1000, null=True, blank=True)
    tag_context = models.TextField(
        null=True, blank=True,
        help_text="Provide any information or context related to variables (like Python-bound variables) that will be "
                  "inserted into the prompt."
    )
    route = models.CharField(
        max_length=100, default='/', help_text="Specify the route or API endpoint for interacting with the bot."
    )

    bot_type = models.CharField(max_length=30, choices=CompanyBotTypeChoices.choices,
                                default=CompanyBotTypeChoices.SIMPLE)
    llm_key = models.CharField(max_length=255, null=True, blank=True)
    dynamic_context = models.TextField(
        null=True, blank=True,
        help_text="Provide dynamic context that can be adjusted during the bot's interactions, such as "
                  "personalized data."
    )
    dynamic_context_type = models.CharField(max_length=20, choices=CompanyBotDynamicContextType.choices,
                                            null=True, blank=True)
    pre_context = models.TextField(
        null=True, blank=True, help_text="Provide pre-context that will be set before the main prompt to shape the "
                                         "conversation."
    )
    tool_context = models.TextField(null=True, blank=True)
    connect_timeout = models.FloatField(default=5.0, help_text="Timeout in seconds for establishing a LLM connection.")
    read_timeout = models.FloatField(default=10.0, help_text="Timeout in seconds for reading a LLM response.")

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
        ]


class Profile(models.Model):

    first_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=1000, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=1000, null=True, blank=True)

    profile_type = models.CharField(max_length=20, choices=ProfileType.choices, default=ProfileType.USER)
    other_params = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.first_name if self.first_name else ""

    def clean(self):
        super().clean()

        if self.phone:
            if len(Profile.objects.filter(phone=self.phone).all()) > 1:
                raise ValidationError({
                        'phone': 'A profile with this phone number already exists.'
                    })

    def save(self, *args, **kwargs):
        if self.password and 'pbkdf2_sha256' not in self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('email',)
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]


class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(Profile, related_name='receiver', on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ChatStatus.choices)

    class Meta:
        indexes = [
            models.Index(fields=['session']),
        ]

