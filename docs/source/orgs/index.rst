==========================================
Sprawy organizacyjne (organisation things)
==========================================

.. note::
    Note that for this moment this site will be written only in polish language, due to the our convenience.

W związku z pracą nad naszym projektem projectksi_ pojawi się wiele spraw związanych z organizacją zadań i pracy.
Z czasem przybędzie mechanizmów i schematów jakimi będziemy się posługiwać, chociaż w tym momencie nie jest ich wiele.
Aby uniknąć bałaganu spiszemy tutaj wszystkie sprawy i schematy ważne według nas - tak, aby projekt nie był w pełni
zależny od nas i nie był skazany na porzucenie (lub poświęcenie dziesiątek godzin na odzyskanie utraconej wiedzy)
gdy któryś z nas zrezygnuje.

.. _projectksi:

Domena
======

Na potrzebuje deweloperskie została wykupiona domena `projectksi.com <http://projectksi.com>`_. Aktualnie można na niej
znaleźć tą dokumentację - pod adresem http://docs.projectksi.com/.

Narzędzia
=========

W pracy używamy rozmaitych narzędzi automatyzujących nasze zadania i uprzejemniających nam życie. Tu zostanie opisane
jakie to narzędzia i jak z nich korzystać (w kontekście naszego projektu):

* github_
* `kanał irc`_
* dokumentacja_

github
------

Jako system kontroli wersji wykorzystujemy git_. Główne repozytorium przechowujemy na publicznym `repozytorium usługi
github`_. Korzystamy także z wbudowanego w *github* `issue tracking system`_. Tam powiny być odnotowywane postępy
we wszystkich zadaniach nad którymi aktualnie pracujemy. W głółnym README projektu powinna być zawsze aktualna pełna
instrukcja instalacji i uruchomienia kodu.

.. _git: http://git-scm.com/
.. _`repozytorium usługi github`: https://github.com/psychowico/projectksi
.. _`issue tracking system`: https://github.com/psychowico/projectksi/issues
__ `repozytorium usługi github`_

kanał irc
---------

Przesiadujemy na kanale #ksi, w sieci NEWNET. Tam wykłócamy się o różne sprawy, dostajemy też automatyczne powiadomienia
o push'ach do `głównego repozytorium`__. Kanał jest otwarty dla wszystkich.

dokumentacja
------------

System narzędzie wspomagające tworzenie dokumentacji wykorzystujemy Sphinx_. Dokumentacja jest przechowywana w głównym
repozytorum, w folderze *docs*.
Po każdym pushu dokumentacja jest automatycznie kompilowana i aktualizowana do najnowszej wersji poprzez
usługę ReadTheDocs_ i dostępna pod adresem http://docs.projectksi.com.

.. _Sphinx: http://sphinx.pocoo.org/
.. _ReadTheDocs: http://readthedocs.org/