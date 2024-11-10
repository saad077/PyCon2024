import yaml
import argparse
import logging
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_template(template_file):
    """Load and return the Jinja2 template."""
    env = Environment(loader=FileSystemLoader('.'))
    try:
        template = env.get_template(template_file)
        logger.info(f"Template loaded from {template_file}")
        return template
    except Exception as e:
        logger.error(f"Failed to load template: {template_file}. Error: {e}")
        raise

def load_configurations(configurations_file):
    """Load and return the configurations from a YAML file."""
    try:
        with open(configurations_file, 'r') as f:
            configurations = yaml.safe_load(f)
        logger.info(f"Configurations loaded from {configurations_file}")
        return configurations
    except Exception as e:
        logger.error(f"Failed to load configurations from {configurations_file}. Error: {e}")
        raise

def get_environment_config(configurations, env_name):
    """Retrieve the configuration for the specified environment."""
    config = configurations.get(env_name)
    if not config:
        logger.error(f"Environment '{env_name}' not found in configurations.")
        raise ValueError(f"Environment '{env_name}' not found in configurations.")
    return config

def update_image_tag(config, image_tag):
    """Update the image tag in the environment configuration."""
    config['image_tag'] = image_tag
    logger.info(f"Using image tag: {image_tag} for environment")
    return config

def render_template(template, config):
    """Render the template with the updated configuration."""
    try:
        rendered_template = template.render(config)
        return rendered_template
    except Exception as e:
        logger.error(f"Failed to render template. Error: {e}")
        raise

def save_rendered_template(rendered_template, env_name):
    """Save the rendered template to a deployment file."""
    deployment_file = f"deployment_{env_name}.yaml"
    try:
        with open(deployment_file, 'w') as f:
            f.write(rendered_template)
        logger.info(f"Deployment YAML for {env_name} written to {deployment_file}")
    except Exception as e:
        logger.error(f"Failed to write deployment YAML. Error: {e}")
        raise

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Render a deployment YAML file from Jinja2 template and configurations")
    parser.add_argument('--environment', required=True, type=str, help='Environment name (e.g., dev, qa, prod)')
    parser.add_argument('--image_tag', required=True, type=str, help='Docker image tag (e.g., 3.0.2)')
    parser.add_argument('--template', type=str, default='deployment_template.j2', help='Jinja2 template file')
    parser.add_argument('--config', type=str, default='configurations.yaml', help='Configurations YAML file')
    
    args = parser.parse_args()

    # Process the deployment rendering
    try:
        template = load_template(args.template)
        configurations = load_configurations(args.config)
        config = get_environment_config(configurations, args.environment)
        updated_config = update_image_tag(config, args.image_tag)
        rendered_template = render_template(template, updated_config)
        save_rendered_template(rendered_template, args.environment)
    except Exception as e:
        logger.error(f"Failed to generate deployment YAML. Error: {e}")

if __name__ == '__main__':
    main()