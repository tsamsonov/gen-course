---
presentation:
  slideNumber: true
---

<!-- slide -->
# Генерализация множеств точечных объектов

Картографические базы данных. Лекция 3

**Тимофей Самсонов**
[tsamsonov@geogr.msu.ru](tsamsonov@geogr.msu.ru)

<!-- slide -->
# Генерализация множеств точечных объектов

**Методы генерализации**

1. Отбор
1. Кластеризация
1. Регионизация

**Аспекты**

1. Параметризация алгоритмов
1. Оценка результатов

<!-- slide -->
# Кластеризация точек

<!-- slide -->
# Алгоритмы кластеризации
1. К средних
2. ISODATA
3. Иерархическая кластеризация
3. Плотностная кластеризация (DBSCAN/OPTICS)

\+ Оценка качества кластаризации

<!-- slide -->
# Метод К средних

1. Установить количество кластеров $K$
2. Выбрать случайным образом $K$ точек в качестве центров кластеров
3. Определить для каждой точки ближайший центр кластера
4. Рассчитать новый центр кластера на основе координат его точек
5. Повторять шаги 3-4, до тех пор пока центры кластеров не перестанут менять свое местоположение.

**Steinhaus H.** (1956). *Sur la division des corps materiels en parties.* Bull. Acad. Polon. Sci., C1. III vol IV: 801—804.

**Lloyd S.** (1957). *Least square quantization in PCM’s.* Bell Telephone Laboratories Paper.

**MacQueen J.** (1967). *Some methods for classification and analysis of multivariate observations.* In Proc. 5th Berkeley Symp. on Math. Statistics and Probability, pages 281—297.

<!-- slide -->
# Метод К средних
Пример с четырьмя кластерами:

![](kmeans.gif){width=600px}

[http://shabal.in/visuals/kmeans/](http://shabal.in/visuals/kmeans/)

<!-- slide -->
# Метод К средних

**Свойства метода**

Метод К средних стремится минимизировать суммарное квадратичное отклонение точек кластеров от центров этих кластеров:
  $$
  V = \sum_{i=1}^{k} \sum_{x_j \in S_I} (x_j - \mu_i)^2
  $$
где $k$ --- число кластеров, $S_i$ --- полученные кластеры, $\mu_i$ --- центры кластеров (центры масс векторов этих кластеров)

**Однако**: не гарантируется достижение глобального минимума суммарного квадратичного отклонения $V$, а только одного из локальных минимумов.

<!-- slide -->
# Метод К средних

**Свойства метода**

Все точки результирующих кластров лежат в пределах ячеек диаграммы Вороного для центров этих кластеров:

![](kmeans_vor.png){width=400px}

[https://moderndata.plot.ly/voronoi-diagrams-in-plotly-and-r/](https://moderndata.plot.ly/voronoi-diagrams-in-plotly-and-r/)

<!-- slide -->
# Метод К средних

**Свойства метода**

Результат зависит от выбора исходных центров кластеров, их оптимальный выбор неизвестен:

![](kmeans-1.png){width=700px}

![](kmeans-2.png){width=700px}

[E.M. Mirkes, K-means and K-medoids applet. University of Leicester, 2011.](http://www.math.le.ac.uk/people/ag153/homepage/KmeansKmedoids/Kmeans_Kmedoids.html)

<!-- slide -->
# Метод К средних

**Свойства метода**

Алгоритм хорошо выделяет только разнесенные в пространстве кластеры выпуклой формы. Пример неудачной кластеризации:

![](kmeans-irr.png){width=500px}


<!-- slide -->
# Метод К средних

**Свойства метода:**

1. Не гарантируется достижение глобального минимума суммарного квадратичного отклонения $V$, а только одного из локальных минимумов.

2. Результат зависит от выбора исходных центров кластеров, их оптимальный выбор неизвестен.

3. Алгоритм хорошо выделяет только кластеры выпуклой формы.

4. Метод может выявлять только заданное количество кластеров, но не их естественное число.

<!-- slide -->
# Метод ISODATA

**ISODATA** означает *Iterative Self-Organizing Data Analysis Technique Algorithm*

Метод начинает работу с одного кластера и выполняет рекурсивное разделение множества вдоль его наиболее протяженной оси до тех пор пока все внутрикластерные расстояния не будут в пределах заданного допуска.

**Ball, Geoffrey H., Hall, David J.** (1965) *Isodata: a method of data analysis and pattern classification* Stanford Research Institute, Menlo Park,United States. Office of Naval Research. Information Sciences Branch

<!-- slide -->
# Метод ISODATA

**Алгоритм:**

1. Установить допустимые значения стандартных отклонений $\sigma_x^{max}$ и $\sigma_y^{max}$.
3. Распределить точки по $k$ стартовым кластерам со случайными центрами. Допустимо принять $k=1$, тогда местоположение кластера не имеет значения.
3. Для каждого кластера вычислить значения выборочного среднего $\mu_x, \mu_y$ и стандартного отклонения $\sigma_x$ и $\sigma_y$ координат по осям $X$ и $Y$.
4. Найти максимальное значение $\sigma$ среди всех вычисленных на данный момент. Если это значение больше соответствующего ему допуска $\sigma_x^{max}$ или $\sigma_y^{max}$, разбить этот кластер на два подкластера, используя разделение по $\mu_x$ или $\mu_y$.
5. Распределить точки по новым кластерам с центрами в $\mu_x$ и $\mu_y$.
5. Повторять шаги 3-4, пока во всех кластерах значения $\sigma_x$ и $\sigma_y$ на станут меньше соответствующих значений $\sigma_x^{max}$ и $\sigma_y^{max}$.

<!-- slide -->
# Метод ISODATA

![**Исходный набор данных** (Ball, Hall, 1965)](isodata-0.png){width=450px}

<!-- slide -->
# Метод ISODATA

![**Размещение исходных центров** (Ball, Hall, 1965)](isodata-1.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Разбиение диаграммой Вороного** (Ball, Hall, 1965)](isodata-2.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Распределение точек по кластерам** (Ball, Hall, 1965)](isodata-3.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Вычисление средней точки** (Ball, Hall, 1965)](isodata-4.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Разделение центров** (Ball, Hall, 1965)](isodata-5.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Разбиение диаграммой Вороного** (Ball, Hall, 1965)](isodata-6.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Распределение точек по кластерам** (Ball, Hall, 1965)](isodata-7.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Вычисление новых центров кластеров** (Ball, Hall, 1965)](isodata-8.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Центры кластеров** после итерации 3 (Ball, Hall, 1965)](isodata-9.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Разбиение кластеров** (Ball, Hall, 1965)](isodata-10.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Распределение точек по кластерам** (Ball, Hall, 1965)](isodata-11.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Вычисление новых центров кластеров** (Ball, Hall, 1965)](isodata-12.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Слияние близких центров** (Ball, Hall, 1965)](isodata-13.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Разбиение на кластеры** (Ball, Hall, 1965)](isodata-14.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Центры кластеров** (Ball, Hall, 1965)](isodata-15.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Центры кластеров и их слияние** (Ball, Hall, 1965)](isodata-16.png){width=500px}

<!-- slide -->
# Метод ISODATA

![**Итоговые центры** (Ball, Hall, 1965)](isodata-17.png){width=500px}

<!-- slide -->
# Метод ISODATA

**По сравнению с К средних:**

1. Не обязательно задавать количество кластеров.

2. Более робастный метод вычисления итоговых кластеров.

3. Точно так же хорошо справляется только с изометричными кластерами.

<!-- slide -->
# Вычисление центров кластеров

**Возможны различные варианты:**

![](cluster_centers.png){width=500px}

<!-- slide -->
# Регионизация точек

<!-- slide -->
# Регионизация точек

**Методы регионизации:**

1. Ограничивающие прямоугольники
2. Выпуклая оболочка
3. Невыпуклые оболочки ($\alpha$-shape, $\chi$-shape)

<!-- slide -->
# Ограничивающий прямоугольник (envelope)

![](envelope.png){width=800px}

- Наиболее простой тип оболочки, который используется в ГИС для описания территориального охвата слоя (*экстент*)

- Для построения в общем случае нужно 4 точки, которые обладают минимальным и максимальным значением координат из всего множества

<!-- slide -->
# Выпуклая оболочка (convex hull)

![](chull.png){width=500px}

- **Выпуклой оболочкой** множества $p$ называется  наименьшее выпуклое множество, содержащее $p$

- Выпуклая оболочка обозначается как $Conv(p)$

- Выпуклая оболочка на плоскости является *пересечением всех полуплоскостей, содержащих* $p$

- Существует несколько алгоритмов построения $Conv(p)$

<!-- slide -->
# Выпуклая оболочка
<div style="display: inline-block; width: 45%; vertical-align: top;">
  **Аналогия**

  Представьте себе лассо,  которое накидывается на  множество гвоздей,  вбитых в доску:

  ![](lasso.png){width=330px}
</div>

<div style="display: inline-block; width: 45%; vertical-align: top; margin-left: 2%">
  **Выпуклое и невыпуклое**

  *Выпуклое множество* в аффинном или векторном пространстве — множество, содержащее вместе с любыми двумя точками соединяющий их отрезок:

  ![](convex_concave.png)
</div>

<!-- slide -->
# Выпуклая оболочка

**Алгоритм Джарвиса**

<div style="display: inline-block; width: 55%; vertical-align: top;">

  1. Найти точку $p_0$ с наименьшим значением координаты $X$. Добавить в результат.
  2. Найти точку $p_1$, образующую наименьший угол поворота по часовой стрелке относительно направления оси $Y$. Добавить в результат.
  3. Найти все оставшиеся точки выпуклой оболочки $p_i, i = 2..k$, выбирая каждый раз такую точку $p_i$, что угол поворота от $p_{i-2} p_{i-1}$ к $p_{i-2} p_{i-1}$ наименьший. Остановиться, когда $p_i = p_0$

</div>

<div style="display: inline-block; width: 40%; vertical-align: top; margin-left: 2%">
  ![](jarvis.png)
</div>

**Jarvis, R. A.** (1973). *On the identification of the convex hull of a finite set of points in the plane*. Information Processing Letters 2: 18–21. doi:10.1016/0020-0190(73)90020-3.


<!-- slide -->
# Выпуклая оболочка

**Алгоритм Джарвиса**

![](jarvis.gif)

**Jarvis, R. A.** (1973). *On the identification of the convex hull of a finite set of points in the plane*. Information Processing Letters 2: 18–21. doi:10.1016/0020-0190(73)90020-3.

<!-- slide -->
# Минимальный по площади ограничивающий прямоугольник

**Минимальный по площади ограничивающий прямоугольник** (*minimum bounding rectangle --- MBR*) является наименьшим по площади среди всех прямоугольников, охватывающих данное множество точек

<div style="display: inline-block; width: 45%; vertical-align: top;">
  ![](mbr.png)
</div>

<div style="display: inline-block; width: 45%; vertical-align: top; margin-left: 2%">
  Согласно теореме Фримана-Шапиро *одна из сторон MBR должна касаться выпуклой оболочки*.

  **Freeman, H.; Shapira, R.** (1975), *Determining the minimum-area encasing rectangle for an arbitrary closed curve*. Communications of the ACM, 18: 409–413, MR 0375828, doi:10.1145/360881.360919.
</div>


<!-- slide -->
# Алгоритм Rotating Calipers

Поворачиваем ограничивающий прямоугольник, совмещая его с одной из сторон выпуклой оболочки. Из них выбираем минимальный по площади.

![](calipers.png){width=700px}

**G.T.Toussaint** (1983). *Solving geometric problems with the rotating calipers*. Proceedings of IEEE MELECON'83, Athens, Greece, May 1983, pp. A10. 02/1-4.

<!-- slide -->
# Альфа-оболочка

**Альфа-оболочка ($\alpha$-shape)** --- обобщение понятия выпуклой оболочки, позволяющее строить оболочки, более точно описывающие форму множества, в том числе и вогнутые оболочки. Альфа-оболочка является площадной компонентой *альфа-комплекса ($\alpha$-complex)*, который строится на основе триангуляции Делоне множества точек.

![](ashape.png){width=700px}

**Edelsbrunner H, Kirkpatrick D, Seidel R **(1983) *On the shape of a set of points in the plane*. IEEE Transactions on Information Theory, 29:551–559. doi: 10.1109/TIT.1983.1056714
