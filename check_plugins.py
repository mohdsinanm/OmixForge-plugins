import sys
import os
import importlib.util
from unittest.mock import MagicMock

class MockPluginBase:
    def name(self): raise NotImplementedError
    def api_version(self): raise NotImplementedError
    def load(self, window, plugin_container): raise NotImplementedError
    def get_widget(self): raise NotImplementedError
    def unload(self): raise NotImplementedError

# Create the mock module structure
mock_src = MagicMock()
mock_plugin_api = MagicMock()
mock_plugin_api.PluginBase = MockPluginBase
mock_plugin_api.API_VERSION = 1

sys.modules["src"] = mock_src
sys.modules["src.core"] = mock_src.core
sys.modules["src.core.plugin_manager"] = mock_src.core.plugin_manager
sys.modules["src.core.plugin_manager.plugin_api"] = mock_plugin_api

mock_qt = MagicMock()
sys.modules["PyQt6"] = mock_qt
sys.modules["PyQt6.QtWidgets"] = mock_qt.QtWidgets
sys.modules["PyQt6.QtCore"] = mock_qt.QtCore
sys.modules["PyQt6.QtGui"] = mock_qt.QtGui

def check_plugin(file_path):
    """
    Dynamically loads the plugin and verifies its behavior.
    """
    errors = []
    module_name = os.path.basename(file_path).replace(".py", "")
    
    try:
        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return [f"Could not load spec for {file_path}"]
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Check for Plugin class
        if not hasattr(module, "Plugin"):
            return ["Missing class Plugin"]
        
        PluginClass = getattr(module, "Plugin")
        
        # Instantiate
        try:
            plugin_instance = PluginClass()
        except Exception as e:
            return [f"Failed to instantiate Plugin class: {e}"]

        # 1. Verify name()
        try:
            name = plugin_instance.name()
            if not isinstance(name, str):
                errors.append(f"Method name() returned {type(name).__name__}, expected str")
            elif not name.strip():
                errors.append("Method name() returned an empty string")
        except Exception as e:
            errors.append(f"Method name() raised exception: {e}")

        # 2. Verify api_version()
        try:
            ver = plugin_instance.api_version()
            if ver is None:
                 errors.append("Method api_version() returned None")
        except Exception as e:
            errors.append(f"Method api_version() raised exception: {e}")
            
        # 3. Verify load() run-through
        #    We pass mocks as arguments.
        try:
            mock_window = MagicMock()
            mock_container = MagicMock()
            plugin_instance.load(mock_window, mock_container)
            
            # Check if it actually registered something
            # plugin_container.add_plugin_widget(name, widget)
            if not mock_container.add_plugin_widget.called:
                errors.append("Plugin did not call plugin_container.add_plugin_widget during load()")
        except Exception as e:
             errors.append(f"Method load() crashed: {e}")
             
        # 4. Verify get_widget()
        try:
            widget = plugin_instance.get_widget()
            if widget is None:
                 pass 
        except Exception as e:
            errors.append(f"Method get_widget() raised exception: {e}")

        # 5. Verify unload()
        try:
            plugin_instance.unload()
        except Exception as e:
            errors.append(f"Method unload() crashed: {e}")

    except Exception as e:
        return [f"Fatal error during verification: {e}"]

    return errors

def main():
    plugins_dir = os.getcwd()
    
    has_errors = False
    print(f"Checking plugins in {plugins_dir} (Dynamic Mode)...\n")

    for filename in sorted(os.listdir(plugins_dir)):
        if filename == os.path.basename(__file__) or filename == "__init__.py":
            continue
        
        if filename.endswith(".py"):
            file_path = os.path.join(plugins_dir, filename)
            errors = check_plugin(file_path)
            
            if errors:
                has_errors = True
                print(f"{filename}: FAILED")
                for err in errors:
                    print(f"    - {err}")
            else:
                print(f"{filename}: OK")

    if has_errors:
        sys.exit(1)
    else:
        print("\nAll plugins passed integrity check.")
        sys.exit(0)

if __name__ == "__main__":
    main()
