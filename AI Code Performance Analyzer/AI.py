import streamlit as st
import ast
import re
import tracemalloc
import cProfile
import io
import pstats
import textwrap

class PerformanceAnalyzer:
    def __init__(self):
        self.bottleneck_rules = [
            self._check_nested_loops,
            self._check_inefficient_string_operations,
            self._check_unnecessary_list_comprehensions,
            self._analyze_memory_usage,
            self._profile_execution_time
        ]
    
    def analyze_code(self, code_snippet):
        """
        Comprehensive code performance analysis
        
        Args:
            code_snippet (str): Python code to analyze
        
        Returns:
            dict: Performance analysis results
        """
        results = {
            'bottlenecks': [],
            'optimization_suggestions': [],
            'memory_usage': None,
            'execution_time': None
        }
        
        try:
            # Parse the AST
            tree = ast.parse(code_snippet)
            
            # Run bottleneck detection rules
            for rule in self.bottleneck_rules:
                rule_results = rule(tree, code_snippet)
                if rule_results:
                    results['bottlenecks'].extend(rule_results)
            
            # Measure memory usage
            tracemalloc.start()
            exec(code_snippet)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            results['memory_usage'] = {
                'current': current,
                'peak': peak
            }
            
            # Profile execution time
            profiler = cProfile.Profile()
            profiler.enable()
            exec(code_snippet)
            profiler.disable()
            
            # Capture profiler stats
            stats_stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=stats_stream)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.print_stats(10)
            
            results['execution_time'] = stats_stream.getvalue()
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _check_nested_loops(self, tree, code_snippet):
        """Detect potentially inefficient nested loops"""
        nested_loops = []
        loop_depth = 0
        max_recommended_depth = 2
        
        class LoopVisitor(ast.NodeVisitor):
            def visit_For(self, node):
                nonlocal loop_depth
                loop_depth += 1
                if loop_depth > max_recommended_depth:
                    nested_loops.append({
                        'type': 'Nested Loops',
                        'description': f'Deep nesting of {loop_depth} loops detected',
                        'suggestion': 'Consider refactoring with list comprehensions or generator expressions'
                    })
                self.generic_visit(node)
                loop_depth -= 1
            
            def visit_While(self, node):
                nonlocal loop_depth
                loop_depth += 1
                if loop_depth > max_recommended_depth:
                    nested_loops.append({
                        'type': 'Nested Loops',
                        'description': f'Deep nesting of {loop_depth} loops detected',
                        'suggestion': 'Consider refactoring to reduce complexity'
                    })
                self.generic_visit(node)
                loop_depth -= 1
        
        LoopVisitor().visit(tree)
        return nested_loops
    
    def _check_inefficient_string_operations(self, tree, code_snippet):
        """Detect inefficient string concatenation"""
        inefficient_ops = []
        
        if '+' in code_snippet and 'str' in code_snippet:
            inefficient_ops.append({
                'type': 'String Concatenation',
                'description': 'Multiple string concatenations detected',
                'suggestion': 'Use str.join() or f-strings for better performance'
            })
        
        return inefficient_ops
    
    def _check_unnecessary_list_comprehensions(self, tree, code_snippet):
        """Check for potentially unnecessary list comprehensions"""
        unnecessary_comps = []
        
        class CompVisitor(ast.NodeVisitor):
            def visit_ListComp(self, node):
                if len(node.generators) > 1:
                    unnecessary_comps.append({
                        'type': 'Complex List Comprehension',
                        'description': 'Multiple generators in list comprehension',
                        'suggestion': 'Consider breaking into separate comprehensions or using explicit loops'
                    })
                self.generic_visit(node)
        
        CompVisitor().visit(tree)
        return unnecessary_comps
    
    def _analyze_memory_usage(self, tree, code_snippet):
        """Additional memory usage analysis"""
        memory_hints = []
        
        if 'append' in code_snippet:
            memory_hints.append({
                'type': 'Memory Usage',
                'description': 'Repeated list.append() can be memory-intensive',
                'suggestion': 'Consider using list comprehensions or generator expressions'
            })
        
        return memory_hints
    
    def _profile_execution_time(self, tree, code_snippet):
        """Basic execution time profiling"""
        time_hints = []
        
        complex_function_patterns = [
            r'def\s+\w+\s*\(.*\):\s*(?:.*\n)*?\s*for\s+',  # Functions with loops
            r'def\s+\w+\s*\(.*\):\s*(?:.*\n)*?\s*while\s+'   # Functions with while loops
        ]
        
        for pattern in complex_function_patterns:
            if re.search(pattern, code_snippet, re.MULTILINE):
                time_hints.append({
                    'type': 'Execution Time',
                    'description': 'Potential long-running function detected',
                    'suggestion': 'Profile and optimize complex functions'
                })
        
        return time_hints

def main():
    # Set up the Streamlit app
    st.set_page_config(
        page_title="AI Code Performance Analyzer", 
        page_icon="🚀",
        layout="wide"
    )
    
    # App title and description
    st.title("🚀 AI Code Performance Analyzer")
    st.markdown("""
    ### Identify Performance Bottlenecks in Your Python Code
    
    - Upload a Python file or paste your code directly
    - Get insights on potential performance issues
    - Receive optimization suggestions
    """)
    
    # Initialize the performance analyzer
    analyzer = PerformanceAnalyzer()
    
    # Sidebar for file upload
    st.sidebar.header("Code Input")
    upload_option = st.sidebar.radio(
        "Choose Input Method", 
        ["Paste Code", "Upload File"]
    )
    
    # Code input
    if upload_option == "Paste Code":
        code_snippet = st.sidebar.text_area(
            "Paste your Python code", 
            height=300
        )
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Choose a Python file", 
            type=['py']
        )
        code_snippet = ""
        if uploaded_file is not None:
            code_snippet = uploaded_file.getvalue().decode("utf-8")
    
    # Analyze button
    if st.sidebar.button("Analyze Performance"):
        if not code_snippet.strip():
            st.error("Please provide a code snippet or upload a file.")
        else:
            # Perform analysis
            with st.spinner('Analyzing your code...'):
                try:
                    results = analyzer.analyze_code(code_snippet)
                    
                    # Display results
                    st.header("Analysis Results")
                    
                    # Bottlenecks
                    if results.get('bottlenecks'):
                        st.subheader("🚨 Potential Bottlenecks")
                        for bottleneck in results['bottlenecks']:
                            st.warning(f"**{bottleneck['type']}**")
                            st.write(f"Description: {bottleneck['description']}")
                            st.info(f"Suggestion: {bottleneck['suggestion']}")
                    
                    # Memory Usage
                    if results.get('memory_usage'):
                        st.subheader("💾 Memory Usage")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Current Memory", 
                                f"{results['memory_usage']['current']} bytes"
                            )
                        with col2:
                            st.metric(
                                "Peak Memory", 
                                f"{results['memory_usage']['peak']} bytes"
                            )
                    
                    # Execution Time Profile
                    if results.get('execution_time'):
                        st.subheader("⏱️ Execution Profile")
                        st.code(results['execution_time'], language='text')
                    
                    # Original Code Preview
                    st.subheader("📝 Original Code")
                    st.code(textwrap.dedent(code_snippet), language='python')
                
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    This tool provides AI-powered performance analysis for Python code.
    
    **Limitations:**
    - Experimental performance detection
    - Primarily focuses on static code analysis
    - May not catch all performance issues
    """)

if __name__ == "__main__":
    main()