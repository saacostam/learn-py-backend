from myapp.features.app import UserUseCases
from myapp.shared.di.app import Context

from .context_impl import ContextImpl

_ctx: Context = ContextImpl()

user_use_cases = UserUseCases(_ctx)
