from providers import UIAssetsManager, MessageBuilderProvider, Settings_Provider
from views import AmicosApp

if __name__ == '__main__':
    message_builder_provider = MessageBuilderProvider()
    settings_provider = Settings_Provider()
    ui_assets_manager = UIAssetsManager()
    
    amicos_app = AmicosApp()
    amicos_app.set_ui_assets_manager(ui_assets_manager)
    amicos_app.set_message_builder_provider(message_builder_provider)
    amicos_app.set_settings_provider(settings_provider)

    amicos_app.run()