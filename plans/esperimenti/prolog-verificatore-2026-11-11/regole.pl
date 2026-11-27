:- encoding(utf8).
% regole.pl — i prerequisiti dei talenti come regole Prolog (SWI-Prolog).
% Esperimento 2026-11-11. I fatti li scrive verifica_prolog.py:
%   dati:   req_car/4, req_bab/3, req_lic/3, req_classe/4, req_talento/3, req_cap/3, cap_da/4
%   scheda: scheda/2, car/3, bab/2, livello/3, dv/2, lic/2, ha/2
% Ogni violazione porta la regola e il controesempio (atteso, ha).

:- discontiguous req_car/4, req_bab/3, req_lic/3, req_classe/4, req_talento/3,
   req_cap/3, cap_da/4, scheda/2, car/3, bab/2, livello/3, dv/2, lic/2, ha/2.
:- discontiguous violazione/5.
:- dynamic req_car/4, req_bab/3, req_lic/3, req_classe/4, req_talento/3,
   req_cap/3, cap_da/4, scheda/2, car/3, bab/2, livello/3, dv/2, lic/2, ha/2.

car_di(F, C, V) :- ( car(F, C, V0) -> V = V0 ; V = 10 ).
liv_di(F, character, N) :- !, ( dv(F, N0) -> N = N0 ; N = 0 ).
liv_di(F, C, N) :- ( livello(F, C, N0) -> N = N0 ; N = 0 ).

% R-CAR  caratteristica sotto la soglia
violazione(F, T, car(C), Atteso, Ha) :-
    ha(F, T), scheda(F, S), req_car(S, T, C, Atteso), car_di(F, C, Ha), Ha < Atteso.
% R-BAB  bonus di attacco base sotto la soglia (BAB ignoto = non si giudica)
violazione(F, T, bab, Atteso, Ha) :-
    ha(F, T), scheda(F, S), req_bab(S, T, Atteso), bab(F, Ha), Ha < Atteso.
% R-LIC  livello d'incantatore
violazione(F, T, lic, Atteso, Ha) :-
    ha(F, T), scheda(F, S), req_lic(S, T, Atteso), ( lic(F, Ha0) -> Ha = Ha0 ; Ha = 0 ), Ha < Atteso.
% R-CLASSE  livelli di una classe (character = livello del personaggio)
violazione(F, T, classe(C), Atteso, Ha) :-
    ha(F, T), scheda(F, S), req_classe(S, T, C, Atteso), liv_di(F, C, Ha), Ha < Atteso.
% R-TALENTO  un talento prerequisito che la scheda non ha
violazione(F, T, talento, P, assente) :-
    ha(F, T), scheda(F, S), req_talento(S, T, P), \+ ha(F, P).
% R-CAPACITA  una capacità di classe che nessuna classe della scheda dà a quel livello
violazione(F, T, capacita, Cap, assente) :-
    ha(F, T), scheda(F, S), req_cap(S, T, Cap),
    \+ ( cap_da(S, Cap, C, L), liv_di(F, C, N), N >= L ).

% R-CATENA (solo Prolog, la chiusura transitiva): un prerequisito di un
% prerequisito che manca, quando il dato non lo ripete già sul talento finale.
richiede(S, T, P) :- req_talento(S, T, P).
richiede(S, T, P) :- req_talento(S, T, Q), richiede(S, Q, P).
violazione(F, T, catena(Q), P, assente) :-
    ha(F, T), scheda(F, S), req_talento(S, T, Q), richiede(S, Q, P),
    \+ req_talento(S, T, P), \+ ha(F, P).

main :-
    forall(violazione(F, T, R, A, H),
           ( format_r(R, RS),
             format("~w\t~w\t~w\t~w\t~w~n", [F, T, RS, A, H]) )).
format_r(R, S) :- term_to_atom(R, S).
