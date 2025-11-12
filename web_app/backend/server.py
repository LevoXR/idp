#!/usr/bin/env python3
"""
Simple HTTP server for Aditya Setu
Uses Python's built-in http.server for localhost access
"""
import os
import json
import secrets
import urllib.parse
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
from pathlib import Path
import bcrypt

# Import database models
from models import init_database, get_db, User, Assessment, Alert


def load_covid_data():
    """Load COVID case data from statw.txt file"""
    covid_data = {}
    try:
        # Path to statw.txt file (relative to project root)
        file_path = Path(__file__).parent.parent / 'statw.txt'
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Skip header lines (first 2 lines)
            for line in lines[2:]:
                line = line.strip()
                # Skip empty lines and separator lines
                if not line or '---' in line:
                    continue
                # Parse the markdown table format
                # Format: | State/UT | Cases |
                parts = [p.strip() for p in line.split('|')]
                # Filter out empty parts (markdown tables have empty first/last parts)
                parts = [p for p in parts if p]
                if len(parts) >= 2:
                    state = parts[0].strip()
                    # Remove commas from numbers and convert to int
                    cases_str = parts[1].strip().replace(',', '').replace(' ', '')
                    try:
                        cases = int(cases_str)
                        covid_data[state] = cases
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error loading COVID data: {e}")
    return covid_data


class AdityaSetuHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Aditya Setu application"""
    
    # Store active sessions (in production, use Redis or database)
    sessions = {}
    
    def do_GET(self):
        """Handle GET requests"""
        path = urllib.parse.urlparse(self.path).path
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Serve static files
        if path.startswith('/static/'):
            self.serve_static(path)
            return
        
        # Route handling
        if path == '/':
            self.serve_index()
        elif path == '/register':
            self.serve_register()
        elif path == '/login':
            self.serve_login()
        elif path == '/dashboard':
            self.serve_dashboard()
        elif path == '/assessment':
            self.serve_assessment()
        elif path == '/alerts':
            self.serve_alerts()
        elif path == '/admin':
            self.serve_admin_dashboard()
        elif path == '/admin/alerts':
            self.serve_admin_alerts()
        elif path == '/logout':
            self.handle_logout()
        elif path.startswith('/api/'):
            self.handle_api_get(path, query_params)
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        path = urllib.parse.urlparse(self.path).path
        
        if path == '/register':
            self.handle_register()
        elif path == '/login':
            self.handle_login()
        elif path == '/assessment':
            self.handle_assessment()
        elif path == '/admin/alerts':
            self.handle_create_alert()
        elif path.startswith('/api/'):
            self.handle_api_post(path)
        else:
            self.send_error(404, "Not Found")
    
    def get_current_user(self):
        """Get current logged-in user from session"""
        session_id = self.get_session_id()
        if session_id and session_id in self.sessions:
            user_id = self.sessions[session_id]
            db = get_db()
            try:
                user = db.query(User).filter_by(id=user_id).first()
                if user:
                    return {
                        'id': user.id,
                        'name': user.name or '',
                        'email': user.email or '',
                        'mobile': user.mobile or '',
                        'is_admin': user.is_admin or False,
                        'age': user.age,
                        'gender': user.gender or '',
                        'location': user.location or ''
                    }
            finally:
                db.close()
        return None
    
    def get_session_id(self):
        """Extract session ID from cookies"""
        cookies = self.headers.get('Cookie', '')
        for cookie in cookies.split(';'):
            if 'session_id' in cookie:
                return cookie.split('=')[1].strip()
        return None
    
    def set_session(self, user_id):
        """Create a new session for user"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = user_id
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        return session_id
    
    def clear_session(self):
        """Clear user session"""
        session_id = self.get_session_id()
        if session_id and session_id in self.sessions:
            del self.sessions[session_id]
        self.send_header('Set-Cookie', 'session_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
    
    def require_auth(self):
        """Check if user is authenticated"""
        user = self.get_current_user()
        if not user:
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return None
        return user
    
    def require_admin(self):
        """Check if user is admin"""
        user = self.require_auth()
        if user and not user.get('is_admin'):
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>403 - Admin Access Required</h1>')
            return None
        return user
    
    def read_post_data(self):
        """Read POST data from request"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        
        post_data = self.rfile.read(content_length).decode('utf-8')
        content_type = self.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            return json.loads(post_data)
        else:
            # Form data
            return urllib.parse.parse_qs(post_data)
    
    def serve_file(self, filepath, content_type='text/html'):
        """Serve a file"""
        try:
            template_path = Path(__file__).parent / 'templates' / filepath
            if template_path.exists():
                with open(template_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, str(e))
    
    def render_template(self, template_name, **context):
        """Enhanced template rendering with Jinja2-like syntax support"""
        import re
        
        template_path = Path(__file__).parent / 'templates' / template_name
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Handle {% extends "base.html" %}
            extends_match = re.search(r'\{%\s*extends\s+["\'](.+?)["\']\s*%\}', content)
            if extends_match:
                base_template = extends_match.group(1)
                base_path = Path(__file__).parent / 'templates' / base_template
                if base_path.exists():
                    with open(base_path, 'r', encoding='utf-8') as f:
                        base_content = f.read()
                    
                    # Extract blocks from current template
                    blocks = {}
                    block_pattern = r'\{%\s*block\s+(\w+)\s*%\}(.*?)\{%\s*endblock\s*%\}'
                    for match in re.finditer(block_pattern, content, re.DOTALL):
                        blocks[match.group(1)] = match.group(2)
                    
                    # Replace blocks in base template
                    for block_name, block_content in blocks.items():
                        block_regex = r'\{%\s*block\s+' + block_name + r'\s*%\}.*?\{%\s*endblock\s*%\}'
                        base_content = re.sub(block_regex, block_content, base_content, flags=re.DOTALL)
                    
                    content = base_content
            
            # Handle {% if ... %}...{% endif %}
            user = context.get('user') or context.get('current_user')
            is_authenticated = user is not None
            is_admin = user is not None and user.get('is_admin', False) if isinstance(user, dict) else (user.is_admin if hasattr(user, 'is_admin') else False)
            
            # Handle {% if current_user.is_authenticated %}...{% else %}...{% endif %}
            if_else_pattern = r'\{%\s*if\s+current_user\.is_authenticated\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
            def replace_if_else(match):
                true_content = match.group(1)
                false_content = match.group(2)
                return true_content if is_authenticated else false_content
            content = re.sub(if_else_pattern, replace_if_else, content, flags=re.DOTALL)
            
            # Handle {% if not current_user.is_authenticated %}...{% else %}...{% endif %}
            if_not_else_pattern = r'\{%\s*if\s+not\s+current_user\.is_authenticated\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
            def replace_if_not_else(match):
                true_content = match.group(1)
                false_content = match.group(2)
                return true_content if not is_authenticated else false_content
            content = re.sub(if_not_else_pattern, replace_if_not_else, content, flags=re.DOTALL)
            
            # Handle {% if current_user.is_authenticated %}...{% endif %} (without else)
            if_pattern2 = r'\{%\s*if\s+current_user\.is_authenticated\s*%\}(.*?)\{%\s*endif\s*%\}'
            content = re.sub(if_pattern2, r'\1' if is_authenticated else '', content, flags=re.DOTALL)
            
            # Handle {% if current_user.is_admin %}
            if_pattern3 = r'\{%\s*if\s+current_user\.is_admin\s*%\}(.*?)\{%\s*endif\s*%\}'
            content = re.sub(if_pattern3, r'\1' if is_admin else '', content, flags=re.DOTALL)
            
            # Handle {% if error %} and {% if success %} blocks
            if_error_pattern = r'\{%\s*if\s+error\s*%\}(.*?)\{%\s*endif\s*%\}'
            has_error = context.get('error', '') and str(context.get('error', '')).strip()
            content = re.sub(if_error_pattern, r'\1' if has_error else '', content, flags=re.DOTALL)
            
            if_success_pattern = r'\{%\s*if\s+success\s*%\}(.*?)\{%\s*endif\s*%\}'
            has_success = context.get('success', '') and str(context.get('success', '')).strip()
            content = re.sub(if_success_pattern, r'\1' if has_success else '', content, flags=re.DOTALL)
            
            # Handle {% if latest_assessment %}...{% else %}...{% endif %}
            if_latest_assessment_pattern = r'\{%\s*if\s+latest_assessment\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
            has_latest = context.get('latest_assessment')
            content = re.sub(if_latest_assessment_pattern, r'\1' if has_latest else r'\2', content, flags=re.DOTALL)
            
            # Handle {% if recent_assessments %}
            if_recent_assessments_pattern = r'\{%\s*if\s+recent_assessments\s*%\}(.*?)\{%\s*endif\s*%\}'
            has_recent = context.get('recent_assessments')
            content = re.sub(if_recent_assessments_pattern, r'\1' if has_recent else '', content, flags=re.DOTALL)
            
            # Handle {% if alerts %}
            if_alerts_pattern = r'\{%\s*if\s+alerts\s*%\}(.*?)\{%\s*endif\s*%\}'
            has_alerts = context.get('alerts')
            content = re.sub(if_alerts_pattern, r'\1' if has_alerts else '', content, flags=re.DOTALL)
            
            # Handle {{ url_for('route') }} - simple URL mapping
            url_for_pattern = r'\{\{\s*url_for\(["\']([^"\']+)["\']\)\s*\}\}'
            url_map = {
                'index': '/',
                'auth.register': '/register',
                'auth.login': '/login',
                'auth.logout': '/logout',
                'assessment.show_assessment': '/assessment',
                'dashboard': '/dashboard',
                'assessment.submit_assessment': '/assessment',
                'alerts': '/alerts',
                'admin.dashboard': '/admin',
            }
            def replace_url_for(match):
                route = match.group(1)
                return url_map.get(route, '/')
            content = re.sub(url_for_pattern, replace_url_for, content)
            
            # Handle {{ variable }} and {{ object.attribute }} substitutions
            # First handle simple variables
            for key, value in context.items():
                var_pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
                content = re.sub(var_pattern, str(value) if value is not None else '', content)
                
                # Handle object attribute access (e.g., {{ user.email }}, {{ current_user.name }})
                if isinstance(value, dict):
                    for attr_key, attr_value in value.items():
                        attr_pattern = r'\{\{\s*' + re.escape(key) + r'\.' + re.escape(attr_key) + r'\s*\}\}'
                        content = re.sub(attr_pattern, str(attr_value) if attr_value is not None else '', content)
                
                # Also handle current_user as alias for user
                if key == 'user' and value:
                    user_pattern = r'\{\{\s*current_user\.(\w+)\s*\}\}'
                    def replace_user_attr(match):
                        attr = match.group(1)
                        if isinstance(value, dict):
                            return str(value.get(attr, ''))
                        elif hasattr(value, attr):
                            return str(getattr(value, attr))
                        return ''
                    content = re.sub(user_pattern, replace_user_attr, content)
            
            # Handle SQLAlchemy objects with method calls like .strftime() and .lower() and filters
            # This pattern handles: {{ object.attribute.method() }} and {{ object.attribute|filter|filter }}
            # Must come BEFORE object_attr_pattern to avoid matching method-less attributes
            object_method_filter_pattern = r'\{\{\s*(\w+)\.(\w+)\.(\w+)\(\)(?:\s*\|\s*(\w+)\([^)]+\))?(?:\s*\|\s*(\w+))?\s*\}\}'
            def replace_object_method_filter(match):
                obj_name = match.group(1)
                attr_name = match.group(2)
                method_name = match.group(3)
                filter1 = match.group(4)
                filter2 = match.group(5)
                obj = context.get(obj_name)
                
                if obj and hasattr(obj, attr_name):
                    attr = getattr(obj, attr_name)
                    if hasattr(attr, method_name):
                        try:
                            result = str(getattr(attr, method_name)())
                            # Apply filters
                            if filter1 == 'replace':
                                # Extract arguments from filter1 like replace('\n', '<br>')
                                result = result.replace('\n', '<br>')
                            if filter2 == 'safe':
                                pass  # No escaping needed for safe
                            return result
                        except:
                            return str(attr)
                    return str(attr)
                return ''
            content = re.sub(object_method_filter_pattern, replace_object_method_filter, content)
            
            # Also handle method calls without filters: {{ object.attribute.method() }}
            object_method_pattern = r'\{\{\s*(\w+)\.(\w+)\.(\w+)\(\)\s*\}\}'
            def replace_object_method(match):
                obj_name = match.group(1)
                attr_name = match.group(2)
                method_name = match.group(3)
                obj = context.get(obj_name)
                
                if obj and hasattr(obj, attr_name):
                    attr = getattr(obj, attr_name)
                    if hasattr(attr, method_name):
                        try:
                            return str(getattr(attr, method_name)())
                        except:
                            return str(attr)
                    return str(attr)
                return ''
            content = re.sub(object_method_pattern, replace_object_method, content)
            
            # Handle object.attribute with filters: {{ object.attribute|replace(...)|safe }}
            object_attr_filter_pattern = r'\{\{\s*(\w+)\.(\w+)(?:\s*\|\s*(\w+)\([^)]*\))?(?:\s*\|\s*(\w+))?\s*\}\}'
            def replace_object_attr_filter(match):
                obj_name = match.group(1)
                attr_name = match.group(2)
                filter1 = match.group(3)
                filter2 = match.group(4)
                obj = context.get(obj_name)
                
                if obj_name in context and isinstance(context[obj_name], dict):
                    return match.group(0)  # Already handled
                
                if obj and hasattr(obj, attr_name):
                    try:
                        attr_value = getattr(obj, attr_name)
                        if isinstance(attr_value, datetime):
                            result = attr_value.strftime('%B %d, %Y at %I:%M %p')
                        else:
                            result = str(attr_value)
                        
                        # Apply filters
                        if filter1 == 'replace':
                            result = result.replace('\n', '<br>')
                        if filter2 == 'safe':
                            pass  # No escaping needed
                        return result
                    except:
                        pass
                return match.group(0)
            content = re.sub(object_attr_filter_pattern, replace_object_attr_filter, content)
            
            # Handle SQLAlchemy objects in loops - convert to dicts for better handling
            # Pattern: {{ object.attribute }} where object is SQLAlchemy
            # Must come AFTER object_method_pattern
            object_attr_pattern = r'\{\{\s*(\w+)\.(\w+)\s*\}\}'
            def replace_object_attr(match):
                obj_name = match.group(1)
                attr_name = match.group(2)
                obj = context.get(obj_name)
                
                # If it's already in context and handled, skip
                if obj_name in context and isinstance(context[obj_name], dict):
                    return match.group(0)
                
                # Try to get attribute from object
                if obj and hasattr(obj, attr_name):
                    try:
                        attr_value = getattr(obj, attr_name)
                        # Handle datetime specially
                        if isinstance(attr_value, datetime):
                            return attr_value.strftime('%B %d, %Y at %I:%M %p')
                        return str(attr_value)
                    except:
                        pass
                return match.group(0)  # Return original if nothing worked
            content = re.sub(object_attr_pattern, replace_object_attr, content)
            
            # Handle {% for ... %} loops - simple implementation
            # Note: This is a basic implementation, complex loops may need adjustment
            for_loop_pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
            def replace_for_loop(match):
                var_name = match.group(1)
                iter_name = match.group(2)
                loop_body = match.group(3)
                
                iterable = context.get(iter_name, [])
                if not isinstance(iterable, list):
                    return ''
                
                result = []
                for item in iterable:
                    if isinstance(item, dict):
                        item_content = loop_body
                        
                        # Handle {% if variable == value %}...{% elif variable == value %}...{% endif %} inside loop (no else)
                        if_elif_pattern = r'\{%\s*if\s+' + var_name + r'\.(\w+)\s*==\s*["\'](.+?)["\']\s*%\}(.*?)\{%\s*elif\s+' + var_name + r'\.(\w+)\s*==\s*["\'](.+?)["\']\s*%\}(.*?)\{%\s*endif\s*%\}' 
                        def handle_if_elif(m):
                            attr1, val1, content1, attr2, val2, content2 = m.groups()
                            # Check first condition
                            if attr1 in item and str(item[attr1]) == val1:
                                return content1
                            # Check second condition
                            elif attr2 in item and str(item[attr2]) == val2:
                                return content2
                            return ''
                        item_content = re.sub(if_elif_pattern, handle_if_elif, item_content, flags=re.DOTALL)
                        
                        # Handle {% if variable == value %}...{% elif variable == value %}...{% else %}...{% endif %} inside loop
                        if_elif_else_pattern = r'\{%\s*if\s+' + var_name + r'\.(\w+)\s*==\s*["\'](.+?)["\']\s*%\}(.*?)\{%\s*elif\s+' + var_name + r'\.(\w+)\s*==\s*["\'](.+?)["\']\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}' 
                        def handle_if_elif_else(m):
                            attr1, val1, content1, attr2, val2, content2, content3 = m.groups()
                            # Check first condition using the item dict
                            if attr1 in item and str(item[attr1]) == val1:
                                return content1
                            # Check second condition
                            elif attr2 in item and str(item[attr2]) == val2:
                                return content2
                            # Else case
                            else:
                                return content3
                        item_content = re.sub(if_elif_else_pattern, handle_if_elif_else, item_content, flags=re.DOTALL)
                        
                        # Handle {% if variable == value %}...{% endif %} inside loop (without elif)
                        if_else_pattern_simple = r'\{%\s*if\s+' + var_name + r'\.(\w+)\s*==\s*["\'](.+?)["\']\s*%\}(.*?)\{%\s*endif\s*%\}' 
                        def handle_if_simple(m):
                            attr, val, content = m.groups()
                            if attr in item and str(item[attr]) == val:
                                return content
                            return ''
                        item_content = re.sub(if_else_pattern_simple, handle_if_simple, item_content, flags=re.DOTALL)
                        
                        # Now handle variable substitutions
                        for key, value in item.items():
                            item_content = re.sub(r'\{\{\s*' + var_name + r'\.' + key + r'\s*\}\}', str(value), item_content)
                            item_content = re.sub(r'\{\{\s*' + key + r'\s*\}\}', str(value), item_content)
                        result.append(item_content)
                    elif hasattr(item, '__class__'):
                        # Handle SQLAlchemy objects
                        item_content = loop_body
                        
                        # Handle method calls in loop: {{ var_name.attr.method() }}
                        method_pattern = r'\{\{\s*' + var_name + r'\.(\w+)\.(\w+)\([^)]*\)\s*\}\}'
                        def handle_method(m):
                            attr, method = m.groups()
                            if hasattr(item, attr):
                                attr_obj = getattr(item, attr)
                                if hasattr(attr_obj, method):
                                    try:
                                        if method == 'strftime':
                                            return attr_obj.strftime('%b %d, %Y %I:%M %p')
                                        return str(getattr(attr_obj, method)())
                                    except:
                                        return str(attr_obj)
                                return str(attr_obj)
                            return ''
                        item_content = re.sub(method_pattern, handle_method, item_content)
                        
                        # Handle simple attributes: {{ var_name.attr }}
                        attr_pattern = r'\{\{\s*' + var_name + r'\.(\w+)\s*\}\}'
                        def handle_attr(m):
                            attr = m.group(1)
                            if hasattr(item, attr):
                                try:
                                    val = getattr(item, attr)
                                    if isinstance(val, datetime):
                                        return val.strftime('%b %d, %Y %I:%M %p')
                                    return str(val)
                                except:
                                    pass
                            return ''
                        item_content = re.sub(attr_pattern, handle_attr, item_content)
                        result.append(item_content)
                    else:
                        item_content = loop_body.replace('{{ ' + var_name + ' }}', str(item))
                        result.append(item_content)
                return ''.join(result)
            
            content = re.sub(for_loop_pattern, replace_for_loop, content, flags=re.DOTALL)
            
            # Process remaining conditionals that might have been missed
            # Handle {% if current_user.is_admin %}...{% else %}...{% endif %}
            if_admin_else_pattern = r'\{%\s*if\s+current_user\.is_admin\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
            def replace_admin_else(match):
                true_content = match.group(1)
                false_content = match.group(2)
                return true_content if is_admin else false_content
            content = re.sub(if_admin_else_pattern, replace_admin_else, content, flags=re.DOTALL)
            
            # Remove any remaining {% ... %} tags (must be done last after all conditionals are processed)
            content = re.sub(r'\{%[^%]*%\}', '', content)
            # Remove any remaining {{ ... }} tags
            content = re.sub(r'\{\{[^}]*\}\}', '', content)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', str(len(content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_static(self, path):
        """Serve static files"""
        file_path = path.lstrip('/')
        self.serve_file(file_path, 'text/css' if file_path.endswith('.css') else 'application/javascript')
    
    def serve_index(self):
        """Serve index page"""
        user = self.get_current_user()
        user_dict = user if user else None
        self.render_template('index.html', current_user=user_dict, user=user_dict)
    
    def serve_register(self):
        """Serve registration page"""
        user = self.get_current_user()
        user_dict = user if user else None
        
        # Get error or success message from query parameters
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        error_msg = urllib.parse.unquote(query_params.get('error', [''])[0]) if 'error' in query_params and query_params.get('error') else ''
        success_msg = urllib.parse.unquote(query_params.get('success', [''])[0]) if 'success' in query_params and query_params.get('success') else ''
        
        self.render_template('register.html', 
                           current_user=user_dict, 
                           user=user_dict,
                           error=error_msg,
                           success=success_msg)
    
    def serve_login(self):
        """Serve login page"""
        user = self.get_current_user()
        user_dict = user if user else None
        
        # Get error or success message from query parameters
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        error_msg = query_params.get('error', [''])[0] if 'error' in query_params else ''
        success_msg = query_params.get('success', [''])[0] if 'success' in query_params else ''
        
        self.render_template('login.html', 
                           current_user=user_dict, 
                           user=user_dict,
                           error=error_msg,
                           success=success_msg)
    
    def serve_dashboard(self):
        """Serve user dashboard"""
        user = self.require_auth()
        if not user:
            return
        
        db = get_db()
        try:
            # Get latest assessment
            latest_assessment = db.query(Assessment).filter_by(user_id=user['id'])\
                .order_by(Assessment.created_at.desc()).first()
            
            # Get recent assessments
            recent_assessments = db.query(Assessment).filter_by(user_id=user['id'])\
                .order_by(Assessment.created_at.desc()).limit(5).all()
            
            # Get active alerts
            alerts = db.query(Alert).filter_by(is_active=True)\
                .order_by(Alert.created_at.desc()).limit(10).all()
            
            # Get fresh user data from database to ensure all fields including location are present
            db_user = db.query(User).filter_by(id=user['id']).first()
            if db_user:
                user_dict = {
                    'id': db_user.id,
                    'name': db_user.name or '',
                    'email': db_user.email or '',
                    'mobile': db_user.mobile or '',
                    'location': db_user.location or '',
                    'age': db_user.age,
                    'gender': db_user.gender or '',
                    'is_admin': db_user.is_admin or False
                }
            else:
                user_dict = {
                    'id': user['id'],
                    'name': user.get('name', ''),
                    'email': user.get('email', ''),
                    'mobile': user.get('mobile', ''),
                    'location': user.get('location', '') or '',
                    'is_admin': user.get('is_admin', False)
                }
            
            # Load COVID data and match user's state
            covid_data = load_covid_data()
            user_state_covid_cases = None
            covid_cases_formatted = None
            if user_dict.get('location'):
                user_state = user_dict['location'].strip()
                # Try exact match first
                if user_state in covid_data:
                    user_state_covid_cases = covid_data[user_state]
                else:
                    # Try case-insensitive match
                    for state, cases in covid_data.items():
                        if state.lower() == user_state.lower():
                            user_state_covid_cases = cases
                            break
                # Format the number with commas
                if user_state_covid_cases:
                    covid_cases_formatted = f"{user_state_covid_cases:,}"
            
            self.render_template('dashboard.html', 
                               user=user_dict, 
                               current_user=user_dict,
                               latest_assessment=latest_assessment,
                               recent_assessments=recent_assessments,
                               alerts=alerts,
                               covid_cases=covid_cases_formatted)
        finally:
            db.close()
    
    def serve_assessment(self):
        """Serve assessment page"""
        user = self.require_auth()
        if not user:
            return
        # Questions for the assessment form - 12 comprehensive questions
        questions = [
            {'id': 'fever', 'question': 'Do you have a fever (temperature above 38°C or 100.4°F)?', 'type': 'yes_no'},
            {'id': 'cough', 'question': 'Do you have a cough or sore throat?', 'type': 'yes_no'},
            {'id': 'shortness_breath', 'question': 'Do you experience shortness of breath or difficulty breathing?', 'type': 'yes_no'},
            {'id': 'fatigue', 'question': 'Do you have unusual fatigue or body aches?', 'type': 'yes_no'},
            {'id': 'loss_taste_smell', 'question': 'Have you experienced loss of taste or smell?', 'type': 'yes_no'},
            {'id': 'travel_history', 'question': 'Have you traveled outside your state in the past 14 days?', 'type': 'yes_no'},
            {'id': 'contact_positive', 'question': 'Have you been in close contact with someone who tested positive for COVID-19?', 'type': 'yes_no'},
            {'id': 'public_transport', 'question': 'Do you use public transportation regularly?', 'type': 'yes_no'},
            {'id': 'chronic_disease', 'question': 'Do you have any chronic medical conditions (diabetes, heart disease, respiratory issues)?', 'type': 'yes_no'},
            {'id': 'household_size', 'question': 'How many people live in your household?', 'type': 'numeric'},
            {'id': 'mask_usage', 'question': 'Do you always wear a mask when outside?', 'type': 'yes_no'},
            {'id': 'vaccinated', 'question': 'Are you fully vaccinated against COVID-19?', 'type': 'yes_no'},
        ]
        user_dict = user if isinstance(user, dict) else {
            'id': user.id, 'name': user.name, 'email': user.email, 
            'is_admin': user.is_admin if hasattr(user, 'is_admin') else False
        }
        self.render_template('assessment.html', user=user_dict, current_user=user_dict, questions=questions)
    
    def serve_alerts(self):
        """Serve alerts page"""
        user = self.require_auth()
        if not user:
            return
        user_dict = user if isinstance(user, dict) else {
            'id': user.id, 'name': user.name, 'email': user.email,
            'is_admin': user.is_admin if hasattr(user, 'is_admin') else False
        }
        self.render_template('alerts.html', user=user_dict, current_user=user_dict)
    
    def serve_admin_dashboard(self):
        """Serve admin dashboard"""
        user = self.require_admin()
        if not user:
            return
        user_dict = user if isinstance(user, dict) else {
            'id': user.id, 'name': user.name, 'email': user.email, 'is_admin': True
        }
        self.render_template('admin_dashboard.html', user=user_dict, current_user=user_dict)
    
    def serve_admin_alerts(self):
        """Serve admin alerts management"""
        user = self.require_admin()
        if not user:
            return
        user_dict = user if isinstance(user, dict) else {
            'id': user.id, 'name': user.name, 'email': user.email, 'is_admin': True
        }
        self.render_template('admin_alerts.html', user=user_dict, current_user=user_dict)
    
    def handle_register(self):
        """Handle user registration"""
        data = self.read_post_data()
        
        name = data.get('name', [''])[0] if isinstance(data.get('name'), list) else data.get('name', '')
        email = data.get('email', [''])[0].lower() if isinstance(data.get('email'), list) else data.get('email', '').lower()
        mobile = data.get('mobile', [''])[0] if isinstance(data.get('mobile'), list) else data.get('mobile', '')
        password = data.get('password', [''])[0] if isinstance(data.get('password'), list) else data.get('password', '')
        
        if not all([name, email, mobile, password]):
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Error: All fields are required</h1>')
            return
        
        db = get_db()
        try:
            # Check if user exists
            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                error_msg = urllib.parse.quote('Email already exists. Please use a different email.')
                self.send_response(302)
                self.send_header('Location', f'/register?error={error_msg}')
                self.end_headers()
                return
            
            # Get optional fields
            age = data.get('age', [''])[0] if isinstance(data.get('age'), list) else data.get('age', '')
            gender = data.get('gender', [''])[0] if isinstance(data.get('gender'), list) else data.get('gender', '')
            location = data.get('location', [''])[0] if isinstance(data.get('location'), list) else data.get('location', '')
            
            # Create user
            new_user = User(
                name=name,
                email=email,
                mobile=mobile,
                age=int(age) if age and age.isdigit() else None,
                gender=gender if gender else None,
                location=location if location else None
            )
            new_user.set_password(password)
            
            db.add(new_user)
            db.commit()
        except Exception as e:
            db.rollback()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<h1>Error: {str(e)}</h1>'.encode('utf-8'))
            return
        finally:
            db.close()
        
        self.send_response(302)
        self.send_header('Location', '/login?success=Registration successful')
        self.end_headers()
    
    def handle_login(self):
        """Handle user login"""
        try:
            data = self.read_post_data()
            
            # Handle both form data (dict of lists) and JSON
            if isinstance(data, dict):
                email = data.get('email', [''])[0].lower() if isinstance(data.get('email'), list) else data.get('email', '').lower()
                password = data.get('password', [''])[0] if isinstance(data.get('password'), list) else data.get('password', '')
            else:
                email = ''
                password = ''
            
            if not email or not password:
                self.send_response(302)
                self.send_header('Location', '/login?error=Email and password are required')
                self.end_headers()
                return
            
            db = get_db()
            try:
                user = db.query(User).filter_by(email=email).first()
                
                if user and user.check_password(password):
                    # Login successful - set session BEFORE sending response
                    session_id = secrets.token_urlsafe(32)
                    self.sessions[session_id] = user.id
                    
                    if user.is_admin:
                        redirect_url = '/admin'
                    else:
                        redirect_url = '/dashboard'
                    
                    self.send_response(302)
                    self.send_header('Location', redirect_url)
                    self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; SameSite=Lax')
                    self.end_headers()
                    return
                else:
                    # Login failed - invalid credentials
                    error_msg = urllib.parse.quote('Invalid email or password. Please try again.')
                    self.send_response(302)
                    self.send_header('Location', f'/login?error={error_msg}')
                    self.end_headers()
                    return
            except Exception as e:
                print(f"Database error during login: {e}")
                error_msg = urllib.parse.quote('An error occurred. Please try again.')
                self.send_response(302)
                self.send_header('Location', f'/login?error={error_msg}')
                self.end_headers()
                return
            finally:
                db.close()
        except Exception as e:
            print(f"Error in handle_login: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<h1>Server Error: {str(e)}</h1>'.encode('utf-8'))
    
    def handle_logout(self):
        """Handle user logout"""
        session_id = self.get_session_id()
        if session_id and session_id in self.sessions:
            del self.sessions[session_id]
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', 'session_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
        self.end_headers()
    
    def handle_assessment(self):
        """Handle assessment submission"""
        user = self.require_auth()
        if not user:
            return
        
        try:
            data = self.read_post_data()
            db = get_db()
            
            # Extract answers from form data
            answers = {}
            for key, value in data.items():
                # Form data comes as lists, so get first element
                if isinstance(value, list):
                    answers[key] = value[0]
                else:
                    answers[key] = value
            
            # Calculate risk score
            risk_score = self.calculate_risk_score(answers)
            
            # Determine risk level
            if risk_score <= 2:
                risk_level = "Low"
            elif risk_score <= 5:
                risk_level = "Moderate"
            else:
                risk_level = "High"
            
            # Generate recommendations
            recommendations = self.generate_recommendations(risk_level, answers)
            
            # Create and save assessment
            assessment = Assessment(
                user_id=user['id'],
                answers=answers,
                risk_score=risk_score,
                risk_level=risk_level,
                recommendations=recommendations
            )
            
            db.add(assessment)
            db.commit()
            
            self.log_message(f"Assessment created: User {user['id']}, Risk: {risk_level}, Score: {risk_score}")
            
            self.send_response(302)
            self.send_header('Location', '/dashboard')
            self.end_headers()
            
        except Exception as e:
            db.rollback()
            import traceback
            self.log_message(f"Error creating assessment: {e}")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<h1>Error: {str(e)}</h1><pre>{traceback.format_exc()}</pre>'.encode('utf-8'))
        finally:
            if 'db' in locals():
                db.close()
    
    def calculate_risk_score(self, answers):
        """Calculate risk score based on assessment answers"""
        score = 0
        
        # High risk symptoms (2 points each)
        if answers.get('fever') == 'yes':
            score += 2
        if answers.get('shortness_breath') == 'yes':
            score += 2
        if answers.get('loss_taste_smell') == 'yes':
            score += 2
        if answers.get('contact_positive') == 'yes':
            score += 2
        
        # Moderate risk symptoms (1 point each)
        if answers.get('cough') == 'yes':
            score += 1
        if answers.get('fatigue') == 'yes':
            score += 1
        if answers.get('travel_history') == 'yes':
            score += 1
        if answers.get('chronic_disease') == 'yes':
            score += 1
        
        # Lifestyle factors
        if answers.get('public_transport') == 'yes':
            score += 1
        
        # Household size risk (1 point if >4 people)
        try:
            household_size = int(answers.get('household_size', '0'))
            if household_size > 4:
                score += 1
        except (ValueError, TypeError):
            pass
        
        # Protective factors (reduce score)
        if answers.get('vaccinated') == 'yes':
            score -= 1
        if answers.get('mask_usage') == 'yes':
            score -= 1
        
        # Ensure score doesn't go below 0
        return max(0, score)
    
    def generate_recommendations(self, risk_level, answers):
        """Generate recommendations based on risk level and answers"""
        recommendations = []
        
        if risk_level == "High":
            recommendations.append("⚠️ HIGH RISK DETECTED")
            recommendations.append("Please seek immediate medical attention.")
            recommendations.append("Contact your healthcare provider or visit the nearest hospital.")
            recommendations.append("Self-isolate immediately and avoid contact with others.")
            if answers.get('vaccinated') != 'yes':
                recommendations.append("Consider getting vaccinated as soon as possible.")
        elif risk_level == "Moderate":
            recommendations.append("⚠️ MODERATE RISK")
            recommendations.append("Monitor your symptoms closely.")
            recommendations.append("Consider consulting with a healthcare professional.")
            recommendations.append("Stay home and avoid unnecessary outdoor activities.")
            recommendations.append("Continue social distancing and wear a mask.")
            if answers.get('vaccinated') != 'yes':
                recommendations.append("Getting vaccinated can help reduce your risk.")
        else:
            recommendations.append("✅ LOW RISK")
            recommendations.append("Continue following health guidelines.")
            recommendations.append("Maintain good hygiene practices.")
            recommendations.append("Wear masks in public places.")
            recommendations.append("Maintain social distancing.")
            if answers.get('vaccinated') != 'yes':
                recommendations.append("Consider getting vaccinated to protect yourself further.")
            else:
                recommendations.append("Good job staying vaccinated! Continue following safety measures.")
        
        # Additional specific recommendations based on symptoms
        if answers.get('fever') == 'yes' or answers.get('cough') == 'yes':
            recommendations.append("Monitor your temperature regularly and stay hydrated.")
        
        if answers.get('chronic_disease') == 'yes':
            recommendations.append("Since you have chronic conditions, be extra careful and consult your doctor regularly.")
        
        return '\n'.join(recommendations)
    
    def handle_create_alert(self):
        """Handle alert creation (admin only)"""
        user = self.require_admin()
        if not user:
            return
        
        data = self.read_post_data()
        # Process and save alert
        # (Implementation details)
        
        self.send_response(302)
        self.send_header('Location', '/admin/alerts')
        self.end_headers()
    
    def handle_api_get(self, path, query_params):
        """Handle API GET requests"""
        if path == '/api/alerts':
            db = get_db()
            try:
                alerts = db.query(Alert).filter_by(is_active=True).all()
                
                result = []
                for alert in alerts:
                    result.append({
                        'id': alert.id,
                        'title': alert.title,
                        'message': alert.message,
                        'target_location': alert.target_location,
                        'created_at': alert.created_at.isoformat() if alert.created_at else None
                    })
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            finally:
                db.close()
    
    def handle_api_post(self, path):
        """Handle API POST requests"""
        self.send_error(501, "Not Implemented")
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        # This doesn't actually send data, just determines the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to a public DNS server (doesn't actually connect)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def get_public_ip():
    """Get the public IP address (for external access)"""
    try:
        import urllib.request
        # Try multiple services in case one is down
        services = [
            'https://api.ipify.org?format=json',
            'https://ifconfig.me/ip',
            'https://ipinfo.io/ip'
        ]
        
        for service in services:
            try:
                if 'json' in service:
                    response = urllib.request.urlopen(service, timeout=3)
                    data = json.loads(response.read().decode())
                    return data.get('ip', None)
                else:
                    response = urllib.request.urlopen(service, timeout=3)
                    return response.read().decode().strip()
            except Exception:
                continue
        return None
    except Exception:
        return None


def run_server(port=8000, host='0.0.0.0'):
    """Run the HTTP server
    
    Args:
        port: Port number to bind to (default: 8000)
        host: Host address to bind to (default: '0.0.0.0' for all interfaces)
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, AdityaSetuHandler)
    
    print(f"Starting Aditya Setu server on http://{host}:{port}")
    if host == '0.0.0.0':
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        
        print(f"\n{'='*60}")
        print("Server Access Information")
        print(f"{'='*60}")
        print(f"  [OK] Local:        http://localhost:{port}")
        print(f"  [OK] Same Network: http://{local_ip}:{port}")
        
        if public_ip:
            print(f"\n  [*] External Network Access:")
            print(f"     Public IP: {public_ip}")
            print(f"     URL:       http://{public_ip}:{port}")
            print(f"\n     [*] WARNING: This will only work if:")
            print(f"        1. Port forwarding is configured on your router")
            print(f"        2. Port {port} is forwarded to {local_ip}:{port}")
            print(f"        3. Your firewall allows external connections")
            print(f"\n     For easier external access, use ngrok:")
            print(f"        python start_with_ngrok.py")
        else:
            print(f"\n  [*] External Network Access:")
            print(f"     Could not determine public IP.")
            print(f"     To access from different networks:")
            print(f"       1. Use port forwarding on your router, OR")
            print(f"       2. Use ngrok: python start_with_ngrok.py")
            print(f"       3. Run: python setup_external_access.py for instructions")
        
        print(f"\n  Note: Make sure your firewall allows connections on port {port}")
        print(f"{'='*60}")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run server - bind to 0.0.0.0 to allow access from any network interface
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    run_server(port, host)

