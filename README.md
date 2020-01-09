# CCB Playbooks

Verifica todas as contas da **CPFL e Sabesp** em aberto de todas instalações da região de Cubatão e envia por e-mail para os interessados, destacando quais estão vencidas.

Pode ser facilmente adaptado para outras empresa que possuam instalações registradas a CPFL ou Sabesp.

## Configurações

Criar os arquivos:
- `vars/cpfl.yml` a partir do exemplo [vars/cpfl.example.yml](vars/cpfl.example.yml)
- `vars/sabesp.yml` a partir do exemplo [vars/sabesp.example.yml](vars/sabesp.example.yml)
- `vars/email.yml` a partir do exemplo [vars/email.example.yml](vars/email.example.yml)

## Crontab

Sugestão para executar os comandos semanalmente:

Abra o crontab: `crontab -e`

E adicione as seguintes linhas:

```bash
# CPFL: Every wed 11 am
0 11 * * 3 cd /PATH/ccb-playbooks/; ansible-playbook playbooks/cpfl.yml
# Sabesp: Every wed 11 am
0 11 * * 3 cd /PATH/ccb-playbooks/; ansible-playbook playbooks/sabesp.yml
```
