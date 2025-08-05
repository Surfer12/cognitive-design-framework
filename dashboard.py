#!/usr/bin/env python3
"""
Real-Time Dashboard for Enhanced Red Team Evaluation Framework

This Streamlit dashboard provides real-time monitoring and visualization of:
- Test execution progress
- Vulnerability detection rates
- Statistical analysis results
- Model comparison metrics
- Interactive result exploration

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import yaml

# Configure Streamlit page
st.set_page_config(
    page_title="Red Team Evaluation Dashboard",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

class RedTeamDashboard:
    """Main dashboard class for red team evaluation monitoring"""
    
    def __init__(self):
        self.results_file = Path("enhanced_results.jsonl")
        self.config_file = Path("test_config.yaml")
        self.data_cache = {}
        self.last_update = None
        
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            st.error(f"Configuration file {self.config_file} not found")
            return {}
    
    def load_test_results(self):
        """Load test results from JSONL file"""
        if not self.results_file.exists():
            return []
        
        results = []
        try:
            with open(self.results_file, 'r') as f:
                for line in f:
                    if line.strip():
                        results.append(json.loads(line))
        except Exception as e:
            st.error(f"Error loading results: {e}")
        
        return results
    
    def load_comprehensive_report(self):
        """Load comprehensive report if available"""
        report_file = Path("enhanced_red_team_results/comprehensive_report.json")
        if report_file.exists():
            try:
                with open(report_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"Error loading comprehensive report: {e}")
        return None
    
    def create_vulnerability_rate_chart(self, df):
        """Create vulnerability rate chart by model and test case"""
        if df.empty:
            return go.Figure()
        
        # Calculate vulnerability rates
        vuln_rates = df.groupby(['model_id', 'prompt_id']).agg({
            'vulnerability_detected': ['count', 'sum']
        }).round(3)
        
        vuln_rates.columns = ['total_tests', 'vulnerabilities']
        vuln_rates['vulnerability_rate'] = vuln_rates['vulnerabilities'] / vuln_rates['total_tests']
        vuln_rates = vuln_rates.reset_index()
        
        # Create heatmap
        pivot_data = vuln_rates.pivot(index='prompt_id', columns='model_id', values='vulnerability_rate')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Reds',
            text=np.round(pivot_data.values, 2),
            texttemplate="%{text:.1%}",
            textfont={"size": 10},
            colorbar=dict(title="Vulnerability Rate")
        ))
        
        fig.update_layout(
            title="Vulnerability Rates by Model and Test Case",
            xaxis_title="Model",
            yaxis_title="Test Case",
            height=400
        )
        
        return fig
    
    def create_severity_distribution_chart(self, df):
        """Create severity distribution chart"""
        if df.empty:
            return go.Figure()
        
        # Mock severity data (would come from actual results)
        severity_data = df.groupby(['model_id', 'vulnerability_detected']).size().reset_index(name='count')
        
        fig = px.bar(
            severity_data,
            x='model_id',
            y='count',
            color='vulnerability_detected',
            title="Vulnerability Detection by Model",
            labels={'vulnerability_detected': 'Vulnerability Detected', 'count': 'Number of Tests'}
        )
        
        return fig
    
    def create_timeline_chart(self, df):
        """Create timeline chart of test execution"""
        if df.empty:
            return go.Figure()
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.floor('H')
        
        timeline_data = df.groupby(['hour', 'model_id']).agg({
            'vulnerability_detected': 'sum',
            'prompt_id': 'count'
        }).reset_index()
        
        timeline_data['vulnerability_rate'] = timeline_data['vulnerability_detected'] / timeline_data['prompt_id']
        
        fig = px.line(
            timeline_data,
            x='hour',
            y='vulnerability_rate',
            color='model_id',
            title="Vulnerability Rate Over Time",
            labels={'vulnerability_rate': 'Vulnerability Rate', 'hour': 'Time'}
        )
        
        return fig
    
    def create_statistical_summary_table(self, report_data):
        """Create statistical summary table"""
        if not report_data or 'statistical_summary' not in report_data:
            return pd.DataFrame()
        
        stats = report_data['statistical_summary']
        model_summaries = stats.get('model_summaries', {})
        
        summary_data = []
        for model_id, summary in model_summaries.items():
            summary_data.append({
                'Model': model_id,
                'Vulnerability Rate': f"{summary.get('overall_vulnerability_rate', 0):.1%}",
                'Total Tests': summary.get('total_tests', 0),
                'Status': 'High Risk' if summary.get('overall_vulnerability_rate', 0) > 0.2 else 
                         'Medium Risk' if summary.get('overall_vulnerability_rate', 0) > 0.1 else 'Low Risk'
            })
        
        return pd.DataFrame(summary_data)
    
    def render_sidebar(self):
        """Render sidebar with controls and filters"""
        st.sidebar.header("🔴 Red Team Dashboard")
        
        # Auto-refresh toggle
        auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
        
        if auto_refresh:
            time.sleep(30)
            st.experimental_rerun()
        
        # Manual refresh button
        if st.sidebar.button("🔄 Refresh Data"):
            st.experimental_rerun()
        
        # Filter controls
        st.sidebar.subheader("Filters")
        
        # Load test results for filtering
        results = self.load_test_results()
        df = pd.DataFrame(results) if results else pd.DataFrame()
        
        if not df.empty:
            # Model filter
            models = df['model_id'].unique() if 'model_id' in df.columns else []
            selected_models = st.sidebar.multiselect(
                "Select Models",
                options=models,
                default=models
            )
            
            # Test case filter
            test_cases = df['prompt_id'].unique() if 'prompt_id' in df.columns else []
            selected_tests = st.sidebar.multiselect(
                "Select Test Cases",
                options=test_cases,
                default=test_cases[:5] if len(test_cases) > 5 else test_cases
            )
            
            # Time range filter
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                min_date = df['timestamp'].min().date()
                max_date = df['timestamp'].max().date()
                
                date_range = st.sidebar.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
            else:
                date_range = None
                selected_models = []
                selected_tests = []
        else:
            selected_models = []
            selected_tests = []
            date_range = None
        
        return {
            'models': selected_models,
            'test_cases': selected_tests,
            'date_range': date_range
        }
    
    def apply_filters(self, df, filters):
        """Apply filters to dataframe"""
        if df.empty:
            return df
        
        filtered_df = df.copy()
        
        # Apply model filter
        if filters['models']:
            filtered_df = filtered_df[filtered_df['model_id'].isin(filters['models'])]
        
        # Apply test case filter
        if filters['test_cases']:
            filtered_df = filtered_df[filtered_df['prompt_id'].isin(filters['test_cases'])]
        
        # Apply date filter
        if filters['date_range'] and len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            if 'timestamp' in filtered_df.columns:
                filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
                filtered_df = filtered_df[
                    (filtered_df['timestamp'].dt.date >= start_date) &
                    (filtered_df['timestamp'].dt.date <= end_date)
                ]
        
        return filtered_df
    
    def render_main_dashboard(self):
        """Render main dashboard content"""
        
        # Header
        st.title("🔴 Red Team Evaluation Dashboard")
        st.markdown("Real-time monitoring of AI model vulnerability testing")
        
        # Load data
        results = self.load_test_results()
        report_data = self.load_comprehensive_report()
        config = self.load_config()
        
        # Apply filters
        filters = self.render_sidebar()
        df = pd.DataFrame(results) if results else pd.DataFrame()
        filtered_df = self.apply_filters(df, filters)
        
        # Key metrics row
        if not filtered_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_tests = len(filtered_df)
                st.metric("Total Tests", total_tests)
            
            with col2:
                if 'vulnerability_detected' in filtered_df.columns:
                    vulnerabilities = filtered_df['vulnerability_detected'].sum()
                    st.metric("Vulnerabilities Found", vulnerabilities)
                else:
                    st.metric("Vulnerabilities Found", "N/A")
            
            with col3:
                if 'vulnerability_detected' in filtered_df.columns and total_tests > 0:
                    vuln_rate = filtered_df['vulnerability_detected'].sum() / total_tests
                    st.metric("Vulnerability Rate", f"{vuln_rate:.1%}")
                else:
                    st.metric("Vulnerability Rate", "N/A")
            
            with col4:
                if 'model_id' in filtered_df.columns:
                    models_tested = filtered_df['model_id'].nunique()
                    st.metric("Models Tested", models_tested)
                else:
                    st.metric("Models Tested", "N/A")
        
        # Charts row
        if not filtered_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    self.create_vulnerability_rate_chart(filtered_df),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    self.create_severity_distribution_chart(filtered_df),
                    use_container_width=True
                )
            
            # Timeline chart
            st.plotly_chart(
                self.create_timeline_chart(filtered_df),
                use_container_width=True
            )
        
        # Statistical summary
        if report_data:
            st.subheader("📊 Statistical Summary")
            summary_df = self.create_statistical_summary_table(report_data)
            if not summary_df.empty:
                st.dataframe(summary_df, use_container_width=True)
        
        # Detailed results
        if not filtered_df.empty:
            st.subheader("🔍 Detailed Results")
            
            # Show recent results
            display_columns = ['timestamp', 'model_id', 'prompt_id', 'vulnerability_detected', 'confidence_score']
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            
            if available_columns:
                recent_results = filtered_df[available_columns].sort_values('timestamp', ascending=False).head(20)
                st.dataframe(recent_results, use_container_width=True)
        
        # Configuration info
        with st.expander("⚙️ Configuration"):
            if config:
                st.json(config)
            else:
                st.write("No configuration loaded")
        
        # Raw data download
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name=f"red_team_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def render_test_management_tab(self):
        """Render test management interface"""
        st.header("🧪 Test Management")
        
        config = self.load_config()
        
        if config and 'test_sources' in config:
            st.subheader("Available Test Sources")
            
            for source_name, source_config in config['test_sources'].items():
                with st.expander(f"📋 {source_name}"):
                    st.write(f"**Description:** {source_config.get('description', 'N/A')}")
                    
                    st.write("**Test Cases:**")
                    for test_case in source_config.get('test_cases', []):
                        st.write(f"- **{test_case['name']}** (Severity: {test_case.get('severity', 'N/A')})")
                        st.write(f"  - Category: {test_case.get('category', 'N/A')}")
                        st.write(f"  - Expected Failure Rate: {test_case.get('expected_failure_rate', 'N/A'):.1%}")
        
        # Test execution controls (placeholder)
        st.subheader("🚀 Test Execution")
        st.info("Test execution controls would be implemented here for production use")
    
    def render_analysis_tab(self):
        """Render detailed analysis interface"""
        st.header("📈 Detailed Analysis")
        
        report_data = self.load_comprehensive_report()
        
        if report_data:
            # Main evaluation results
            if 'main_evaluation' in report_data:
                st.subheader("Main Evaluation Results")
                main_eval = report_data['main_evaluation']
                
                st.write(f"**Models Tested:** {', '.join(main_eval.get('models_tested', []))}")
                st.write(f"**Test Cases:** {main_eval.get('test_cases', 'N/A')}")
            
            # Statistical summary
            if 'statistical_summary' in report_data:
                st.subheader("Statistical Analysis")
                stats = report_data['statistical_summary']
                
                # Cross-model analysis
                if 'cross_model_analysis' in stats:
                    cross_analysis = stats['cross_model_analysis']
                    st.write(f"**Most Vulnerable Model:** {cross_analysis.get('most_vulnerable_model', 'N/A')}")
                    st.write(f"**Average Vulnerability Rate:** {cross_analysis.get('average_vulnerability_rate', 0):.1%}")
            
            # Mitigation recommendations
            if 'mitigation_recommendations' in report_data:
                st.subheader("🛡️ Mitigation Recommendations")
                for i, rec in enumerate(report_data['mitigation_recommendations'], 1):
                    st.write(f"{i}. {rec}")
        else:
            st.info("No comprehensive report available. Run a complete evaluation to generate detailed analysis.")
    
    def run(self):
        """Run the dashboard application"""
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧪 Test Management", "📈 Analysis"])
        
        with tab1:
            self.render_main_dashboard()
        
        with tab2:
            self.render_test_management_tab()
        
        with tab3:
            self.render_analysis_tab()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "**Enhanced Red Team Evaluation Framework** | "
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

def main():
    """Main function to run the dashboard"""
    dashboard = RedTeamDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()