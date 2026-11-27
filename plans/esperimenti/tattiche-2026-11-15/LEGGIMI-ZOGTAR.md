# Zog'tar sulla breccia dell'alba: simulazione e revisione (15/11/2026)

> Esito delle card del 15/11: il DM ha scelto «separa e finisce» e Balvar e il
> sacerdote al campo all'alba. Il testo è nella Scena 10 di ARC07-DEF-4 e nel §8 del
> BARILE. Il motore `simula_scontri.py` è in `../tattiche-draghi-2026-11-15/` (#450).

Scena: ARC07-DEF-4 Scena 10, «Come combatte sulla breccia» (r.3220), con 0-1
successi sulle mura. Script: `profili_villain.py` (profili sul motore comune
`../tattiche-draghi-2026-11-15/simula_scontri.py`, non copiato). Esiti completi
in `ESITI-ZOGTAR.md`, 20.000 prove per riga, seme 1372.

## Dati e stime
- **Zog'tar**: Appendice A.2 senza numeri nuovi. In Ira 283 + 45 pf, CA 24,
  ascia +29/+24/+19 (3d6+20), RD 3/—, Presenza Minacciosa CD 21, Occhio di
  Ossidiana, Colpo Terrificante. Sul camminamento si stringe: −4/−4 (SRD).
- **Dopo il barile**: 249 pf (mediana di BARILE §7) + 15 di riposo naturale
  (SRD, 1 pf per livello in una notte) = 264. Il sacerdote non ha cure
  preparate (scheda A.2), quindi non lo cura.
- **PG**: carta del 05/11. STIMA i bonus d'attacco di Thorik e Tordek (`--buff 4`
  cambia poco). Thorik immune alla Presenza (Corona).
- **Fuori dal modello**: le quattro guardie in fondo alla scala, le balestre
  dell'orda su chi vola, Re Thorek e Hrodgar, i PG che scendono alle spalle. La
  vulnerabilità di Zog'tar alla luce divina della Corona non ha un numero nella
  scheda: non c'è.

## Che cosa dice la misura
1. **Sulla breccia Zog'tar muore quasi sempre, in 3 round.** Stretto a CA 20,
   con Artemis e Hella che lo colpiscono dall'alto e due nani davanti, perde più
   di 100 pf a round. È un preludio, non un boss: va detto al DM.
2. **La tattica del canone è la più gentile.** Il Colpo Terrificante su chi gli
   sta davanti uccide un PG nell'11% delle prove e lascia ai PG l'81% dei pf per
   il drago. È voluto (boost log del 07/10: «un colpo che separi il gruppo»).
3. **Separare e finire** (Occhio su Tordek, Colpo che butta Thorik giù nel
   cortile, poi attacco completo −5/+10 su Tordek rimasto solo): 28% di prove
   con un PG morto, 76% dei pf rimasti. È quello che fa un generale con INT 16
   che al primo round ha visto Thorik non piegarsi alla sua Presenza.
4. **Lo stringersi vale più della tattica.** Se Zog'tar combatte fuori dal
   camminamento (per esempio nella breccia ceduta, a terra), le morti salgono
   dal 11% al 33% con la stessa tattica, e al 69-73% con l'attacco pieno.

## Cosa sa all'alba, dalla notte del barile (dal canone, nessuna scelta nuova)
| Fatto della notte | Fonte | Che cosa cambia sulla breccia |
|---|---|---|
| Sa che i nani volano e vengono dall'alto | BARILE B21, «Dall'alto. Hanno ali.» | Le guardie in fondo alla scala guardano in alto e tengono i giavellotti per chi vola; lui non lascia la breccia per inseguire (già scritto) |
| È ustionato: 264 pf invece di 283 | BARILE §7, SRD riposo | Il conto dei pf parte da lì |
| Le guardie sono bruciate: 20-23 pf l'una, più 8 di riposo | BARILE §7 | Chi scende alle spalle le trova a metà |
| Il sacerdote è morto una volta su tre | BARILE §7 | Nessun cambio sulla breccia: non ci sale comunque (DEF-4 r.3211) |
| Thorik non si piega alla Presenza | A.2, Corona | Lo vede al primo round: da lì sa chi deve togliere dalla linea |

## Contraddizioni trovate, con la prova
- BARILE r.711 «Balvar sta sulla collina col drago, come nel canone» contro
  DEF-4 r.906 («Balvar resta nella tenda», canone del 12/10) e r.3211 (canone
  Q41 del 07/10). Card a Jfs, consigliata: al campo.
- BARILE r.712 «il sacerdote sale sulla breccia con Zog'tar» contro DEF-4
  r.3211 («senza Balvar e senza il sacerdote, rimasti al campo»). Stessa card.
- BARILE r.712 «cura chi brucia fino a finire gli incantesimi»: la scheda del
  sacerdote (A.2, canone Q26) non ha cure preparate. Si corregge con la prova.
