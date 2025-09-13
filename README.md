# Check list

## Pré-requisitos do Código Original
- [X] Biblioteca curses importada
- [X] Função mover() com sistema de movimentação básico
- [X] Funções safeAddstr() e safeAddch() para desenho seguro
- [X] Estrutura principal com main(stdscr) e curses.wrapper()
- [X] Sistema de loop principal com stdscr.getch()
- [X] Controle de tamanho de terminal
- [X] Simplificar o codigo e eliminar redundancias

## Sistema de Mapa
- [ ] Definir estrutura de dados para o mapa (matriz ou lista de strings)
- [ ] Criar mapa maior que a viewport (ex: 50x50 ou maior)
- [ ] Implementar diferentes tipos de terreno (grama, água, paredes, etc.)
- [ ] Sistema de colisão baseado no tipo de terreno

## Sistema de Viewport/Câmera
- [ ] Definir tamanho fixo da viewport (ex: 19x19)
- [ ] Implementar função para calcular a área visível do mapa
- [ ] Manter jogador sempre no centro da viewport
- [ ] Tratar casos quando jogador está nas bordas do mapa

## Sistema de Renderização
- [ ] Modificar loop de desenho para mostrar apenas o viewport
- [ ] Converter coordenadas do mapa para coordenadas de tela
- [ ] Manter informações do jogador abaixo da viewport
- [ ] Implementar sistema para diferentes caracteres visuais

## Sistema de Movimentação
- [ ] Adaptar função mover() para verificar colisões com o mapa
- [ ] Implementar movimento suave dentro do mapa grande
- [ ] Manter registro da posição absoluta do jogador no mapa

## Melhorias e Funcionalidades Extras
- [ ] Sistema de carregamento de mapa from arquivo
- [ ] Diferentes caracteres para diferentes terrenos
- [ ] Sistema de cores para diferentes elementos
- [ ] Scroll suave da câmera (opcional)
- [ ] Elementos dinâmicos no mapa (NPCs, itens)

## Testes e Validações
- [ ] Testar movimentação nas bordas do mapa
- [ ] Verificar renderização com diferentes tamanhos de terminal
- [ ] Validar sistema de colisões com diferentes terrenos
- [ ] Testar com mapas de diferentes tamanhos

## Documentação
- [ ] Comentar o código explicando o sistema de viewport
- [ ] Documentar formato do arquivo de mapa (se implementar)
- [ ] Listar controles e características do jogo

## Otimizações
- [ ] Otimizar renderização para mapas muito grandes
- [ ] Implementar redimensionamento de terminal em tempo real
- [ ] Adicionar sistema de debug para visualizar coordenadas