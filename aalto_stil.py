fig.update_layout(
        yaxis=dict(
            range=[-2.5, 2.5], 
            fixedrange=True, # Estää skaalautumisen
            gridcolor='lightgray'
        ),
        xaxis=dict(
            range=[0, 2 * np.pi], 
            fixedrange=True, # Estää sivuttaisen hyppimisen
            gridcolor='lightgray'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        # Nämä kaksi riviä poistavat Plotlyn omat animaatio-viiveet, jotka aiheuttavat nykimistä:
        hovermode=False,
        transition_duration=0 
    )
