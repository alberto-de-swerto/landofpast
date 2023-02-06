# Игра 2D: «Land of the past» («Земля прошлого»)
### Автор: Мухутдинов Альберт г.Пермь
### Жанр игры: лабиринт
![изображение](https://user-images.githubusercontent.com/63464936/216998038-7e40a96d-b0f2-414e-a37d-e23ad26c7509.png)
### Идея:  Действие игры происходит в двух мирах: мир юрского периода и подземный мир. Герой игры – мальчик Коля, который волею судеб попал в доисторическое пространство, где встретил Мамонтенка «Димку» (знаменитый мамонтенок музея «Пермских древностей»). В этом мире ему необходимо найти ключи, чтобы открыть дверь в царство камней (в подземелье). В подземелье нашему герою необходимо отыскать минералы, если все минералы собраны, игра пройдена. Герою Кольке нужно быть осторожным, ведь на пути его ожидают различные препятствия: камни, тупики и пауки. 
![изображение](https://user-images.githubusercontent.com/63464936/216998108-a9fa4e6f-a7c7-411f-a3f6-644f8564625c.png)
### Описание реализации: Однопользовательская игра лабиринт, создана в PyCharm с использованием библиотеки Pygame, Pytmx. Создание карты лабиринта осуществлено при помощи Tiled Map Editor. В игре используется вид ортогональной карты, в процессе разработки были использованы готовые тайлы с раширением .png с сайта  https://opengameart.org/ размером 16*16. В игру были встроены диалоги, кнопка «Выход» и «Продолжить», столкновения с врагами (пауки), откат игрока на начало игры, и переход на другой уровень, непрерывное перемещение игрока с помощью стрелок по карте, сбор предметов, ведение счетчика с отображением результата. Игра состоит из двух уровней, хранящихся в папке /maps.
![изображение](https://user-images.githubusercontent.com/63464936/216998206-b5ca3b0f-4ed6-4297-b0c1-f37910f0152c.png)
## В игре использованы классы:
# Labyrinth
# Hero
# Game
