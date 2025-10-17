from providers import UIAssetsManager
from providers import MessageBuilderProvider
from providers import Settings_Provider
from profiles_manager import ProfilesManagerProvider
from views import AmicosApp

if __name__ == '__main__':
    message_builder_provider = MessageBuilderProvider()
    profiles_manager_provider = ProfilesManagerProvider()
    # Despite being an async function, init_db can be run here
    # without a thread.
    profiles_manager_provider.init_db()
    settings_provider = Settings_Provider()
    ui_assets_manager = UIAssetsManager()
    current_user = profiles_manager_provider.get_current_user()
    
    amicos_app = AmicosApp()
    current_platform = amicos_app.get_platform()
    message_builder_provider.set_platform(current_platform)
    amicos_app.set_current_user(current_user)
    amicos_app.set_ui_assets_manager(ui_assets_manager)
    amicos_app.set_message_builder_provider(message_builder_provider)
    amicos_app.set_profiles_manager_provider(profiles_manager_provider)
    amicos_app.set_settings_provider(settings_provider)

    amicos_app.run()