from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatStatus(models.TextChoices):
    STARTED = 'STARTED', _('STARTED')
    IN_PROGRESS = 'IN_PROGRESS', _('IN_PROGRESS')
    COMPLETED = 'COMPLETED', _('COMPLETED')


class LLMModel(models.TextChoices):
    GPT4 = 'gpt-4', _('GPT4')
    GPT4_128K = 'gpt-4-1106-preview', _('GPT4-128k')
    GPT4_TURBO = 'gpt-4-turbo', _('GPT4_TURBO')
    GPT4_O = 'gpt-4o', _('GPT4_O')
    GPT4_O_MINI = 'gpt-4o-mini', _('GPT4_O_MINI')
    GPT4_1 = 'gpt-4.1', _('GPT4_1')
    GPT4_1_MINI = 'gpt-4.1-mini', _('GPT4_1_MINI')
    O1 = 'o1', _('O1')
    O1_PREVIEW = 'o1-preview', _('O1 Preview')
    O1_MINI = 'o1-mini', _('O1 Mini')
    O3 = 'o3', _('O3')
    O3_MINI = 'o3-mini', _('O3_MINI')

class LLMProvider(models.TextChoices):
    BEDROCK = 'bedrock', _('BEDROCK')
    BEDROCK_CONVERSE = 'bedrock/converse', _('BEDROCK_CONVERSE')
    OPENAI = 'openai', _('OPENAI')


class CompanyBotTypeChoices(models.TextChoices):
    SIMPLE = 'SIMPLE', _('SIMPLE')
    STATE_MACHINE = 'STATE_MACHINE', _('STATE_MACHINE')
    DATABASE_SIMPLE = 'DATABASE_SIMPLE', _('DATABASE_SIMPLE')
    INTERVIEW_STATE_MACHINE = 'INTERVIEW_STATE_MACHINE', _('INTERVIEW_STATE_MACHINE')


class CompanyBotDynamicContextType(models.TextChoices):
    SQL_QUERY = 'SQL_QUERY', _('SQL_QUERY')
    PYTHON_SCRIPT = 'PYTHON_SCRIPT', _('PYTHON_SCRIPT')


class ProfileType(models.TextChoices):
    USER = 'USER', _('USER')
    MODERATOR = 'MODERATOR', _('MODERATOR')
    PROSPECT = 'PROSPECT', _('PROSPECT')
