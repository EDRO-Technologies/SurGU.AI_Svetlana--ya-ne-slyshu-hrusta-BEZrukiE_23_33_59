from igraph import Graph, EdgeSeq
import plotly.graph_objects as go


class MindMap:
    """
    Визуализатор интеллект-карт

    Example
    -------
    >>> from TakVamVidno.visualization import MindMap
    >>> from PIL import Image
    >>> from io import BytesIO
    >>> data = {
    ...     "main_topic": "Hello world",
    ...     "subtopics": {
    ...         "subtopic1": ["details1.1", "details1.2"],
    ...         "subtopic2": ["details2"],
    ...         "subtopic3": ["details3.1", "details3.2", "details3.3"],
    ...     },
    ... }
    >>> bytes = MindMap().visualize(...)
    >>> Image.open(BytesIO(bytes)).show()
    """

    def visualize(self, main_topic: str, subtopics: dict[str, list[str]]) -> bytes:
        """
        Создаёт интеллект-карту основываясь на данных.

        Детали подидеи должны быть уникальны.

        Argumemnts
        ----------
        main_topic : str
            Основная идея

        subtopics : dict[str, dict[str, list[str]]]
            Подидеи и их детали.

        Known Issues
        ------------
        - Иногда igraph решает поставить root-node не основную идеи, а подидею, что немного портит внешний вид и вредит усваиванию информации

        TODO
        ----
        - Кастомизацию, позволить менять ориентацию куда идёт график, цвета блоков, итд.
        - Сделать возможность продлевать это древо, щас максимальная глубина это 3 (основная идея -> подидея -> детали), надо сделать это динамическим.
        """

        count, connections, v_label = self._convert_to_connections(
            {"main_topic": main_topic, "subtopics": subtopics}
        )

        G = Graph.TupleList(connections)
        lay = G.layout("rt")

        position = {k: lay[k] for k in range(count)}
        Y = [lay[k][1] for k in range(count)]
        M = max(Y)

        E = [e.tuple for e in G.es]

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2 * M - position[k][1] for k in range(L)]
        Xe = []
        Ye = []

        for edge in E:
            Xe += [position[edge[0]][0], position[edge[1]][0], None]
            Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

        labels = v_label

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=Xe,
                y=Ye,
                mode="lines",
                line=dict(color="rgb(210,210,210)", width=1),
                hoverinfo="none",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=Xn,
                y=Yn,
                mode="markers",
                name="bla",
                marker=dict(
                    symbol="square",
                    size=60,
                    color="#6175c1",
                    line=dict(color="rgb(50,50,50)", width=1),
                ),
                text=labels,
                hoverinfo="text",
                opacity=0.8,
            )
        )

        def make_annotations(pos, text, font_size=10, font_color="rgb(250,250,250)"):
            L = len(pos)
            if len(text) != L:
                raise ValueError("The lists pos and text must have the same len")
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        text=labels[k],
                        x=pos[k][0],
                        y=2 * M - position[k][1],
                        xref="x1",
                        yref="y1",
                        font=dict(color=font_color, size=font_size),
                        showarrow=False,
                    )
                )
            return annotations

        axis = dict(
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        )

        fig.update_layout(
            title="Интеллект-карта",
            annotations=make_annotations(position, v_label),
            font_size=12,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,
            margin=dict(l=40, r=40, b=85, t=100),
            hovermode="closest",
            plot_bgcolor="rgb(248,248,248)",
        )

        return fig.to_image("webp")

    def _convert_to_connections(
        self, data: dict[str, str | dict[str, list[str]]]
    ) -> tuple[int, list[tuple[int, int]], list[str]]:
        """
        Превращает dict с данными в соединения в виде `(main_topic, subtopic)`, `(subtopic, detail)`, итд.
        """
        main_topic = data["main_topic"]
        connections = []
        labels = [main_topic]
        for subtopic, details in data["subtopics"].items():
            connections.append((main_topic, subtopic))
            labels.append(subtopic)
            for detail in details:
                connections.append((subtopic, detail))
                labels.append(detail)
        return len(labels), connections, labels
