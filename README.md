### jrpg-sul-terminale (progetto di fine anno)

un semplice gioco in stile JRPG, eseguito sul terminale di Windows/Linux.

## COME ESEGIURE IL PROGRAMMA
**per prima cosa** si deve verificare se su visual studio si abbia creato una **venv** (virtual enviorment).

### **SOLO SE** non si ha un **venv**
scrivere su un **terminale** il seguente codice,

***al posto di .venv si può chiamarlo come si vuole, basta che DOPO si ricordi di mettere il nome che gli si ha assegnato***

```
python3.11 -m venv .venv
```
***il comando funziona solo in un terminale con python***

se non funziona verificare come si ha chiamato il file eseguibile di python e inserire quello al posto del ***python3.11***.

## DOPO AVER CREATO LA **venv**

```python
#windows
source .venv\Scripts\activate

#linux
source .venv/bin/activate
```

## INSTALLARE I REQUISITI
```python
pip install -r requirements.txt
```
## DOPO AVER LETTO I PASSAGGI PRECEDENTI...
eseguire il file ***inizio_run.py***