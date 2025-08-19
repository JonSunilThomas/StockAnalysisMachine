# frontend/ui_components/display_info.py
import streamlit as st

def display_prediction_and_drivers(prediction_data, explanation_df):
    """
    Displays the prediction metric and the key drivers in a Streamlit column.
    """
    st.subheader("Key Drivers of Prediction")
    forecast = prediction_data['prediction']
    confidence = prediction_data['confidence']
    delta_text = "Upward Trend Expected" if forecast == 'Bullish' else "Downward Trend Expected"
    
    st.metric(
        label="Directional Forecast", 
        value=forecast, 
        delta=delta_text,
        delta_color=("normal" if forecast == 'Bullish' else "inverse")
    )
    
    progress_value = int(confidence * 100)
    st.progress(progress_value, text=f"Confidence: {confidence:.1%}")

    st.subheader("Key Drivers of Prediction")
    st.dataframe(explanation_df, use_container_width=True, hide_index=True)

    explanation_df_for_plot = explanation_df.set_index('feature')
    st.bar_chart(explanation_df_for_plot['contribution'])