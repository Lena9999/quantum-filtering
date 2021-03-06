# quantum-filtering
Quantum implementation of weighted average filter
Данный код написан для проверки роботоспособности предложенной схемы средневзвешенного фильтра. Для проверки работоспособности схемы необходимо запустить следующие модули: умножение и деление на два, доступ к соседям пикселя, сложение изображений. Для создания полной схемы необходимо $9(4 + q) + 2n + 4$ кубит. Для проверки работоспособности построенных схем используются симуляторы квантовых вычислительных устройств. Симуляция поведения квантовой системы с большим количеством кубит вычислительно затратна, и в настоящий момент не представляется возможной при количестве кубит более 30. Чтобы проверить работоспособность предложенной схемы, задача была разделена на две части, соответсвующая двум файлам: sum, multiply. Опишем каждую из них подробнее.

## SUM

Файл под названием sum проверяет наиболее сложные модули: модуль доступа к соседям пикселя и модуль сложения. Для реализации процедуры вызываются три вспомогательные фунуции: реализация квантового представления изображений NEQR (build_neqr_test), сдвг по оси x или y на +1 (shifting_plus), сдвиг по оси на -1 (shifting_minus). Для начала создаются все регистры, в которые будут помещаться копии изображений; их должно быть 9 (размер маски фильтра). Однако, кубит достаточно только на кодирование 8 изображений (что не влияет на проверку работоспособности предложенного алгоритма). В сумме не участвует изображение, которое отвечает за центральный пиксель (значение в центре маски = 0). После создания необходимых 8 регистров для хранения значений пикселей и 1 регистра для хранения местоположения пикселей, происходит помещение соответствующих копий изображения в эти регистры. Каждая копия обрабатывается индивидуально. Для начала туда помещается оригинальное изображение с помощью функции build_neqr_test, а затем производится соответствующий сдвг с помощью shifting_plus или shifting_minus. После того как все необходимое изображения помещаются в соответсвующие регистры, релизуется сумма с помощью последовательного навешивания на соответсвующие регистры функции DraperQFTAdder. Конечный результат находится в последнем изображении. 

В условиях ограниченного количества кубит, в качестве значений пикселя требуется использовать градации серого, которые помещаются в три разряда. Также требуется учитывать, что схема не использует дополнительные кубиты, которые бы учитывали тот факт, что значение пикселя во время суммирования может не поместиться в три разряда. Поэтому значения пикселей требуется выбирать так, чтобы их сумма помещалась в заданное количество кубит.

Для извлечения результата производится измерение с использованием симулятора. Работа с интерпретацией полученных значений заключается в извлечении наиболее вероятных состояний. Затем, значения из двоичной системы переводятся в десятичную. 


## MULTIPLY 

В данном случае проверялась работоспособность предложенных схем для умножения и деления на два. Для этого, как и ранее, выделяется два регистра, для хранения двух изображений (этого достаточно для проверки работоспособности схем), 4 кубита для реализации умножения и деления на два, и регистр для хранения местоположения двух изображений. В один из регистров помещается оригинал изображения с помощью build_neqr_test, и производится сдвиг по обоим координатам с помощью shifting_plus (таким образом получаем соседа с координатами x+1, y+1). Затем, в регистр, отвечащий за значение пикселя второго изображения, помещается оригинал изображения. После, с помощью операции swap, кубиты, которые выделялись для реализации умножения передвигаются таким образом, чтобы множить первое изображение со сдвигом на 2, а изображение без сдвига на 4. После чего к регистрам, отвечающим за значение пикселя применяется операция суммы (DraperQFTAdder). Затем, к регистру, который хранит сумму применяется оператор swap, выполняющий деление суммы изображений на 2. В результате мы получаем свертку изображения со следующей маской, с последующим делением на 2:

|   |   |   | 
|---|---|---|
| 2 | 0 | 0 |
| 0 | 4 | 0 | 
| 0 | 0 | 0 | 
|   |   |   | 






