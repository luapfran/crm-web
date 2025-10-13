-- =====================================================
-- DADOS FICTÍCIOS PARA SISTEMA CRM
-- =====================================================
-- Este script popula o banco com dados de exemplo
-- 10 Clientes + Interações + Cotações + Pedidos
-- =====================================================

-- Limpa dados existentes (CUIDADO: apaga tudo!)
-- TRUNCATE TABLE pedidos RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE cotacoes RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE interacoes RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE clientes RESTART IDENTITY CASCADE;

-- =====================================================
-- INSERÇÃO DE CLIENTES (ATUALIZADO: inclui coluna 'endereco')
-- =====================================================

INSERT INTO clientes (nome, telefone, email, limite_credito, area_atuacao, canal_vendas, endereco, data_cadastro, ultimo_contato, ativo) VALUES
-- Cliente 1
('Tech Solutions Ltda', '(11) 98765-4321', 'contato@techsolutions.com.br', 15000.00, 'Tecnologia da Informação', 'Indústria', 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP', '2024-01-15', '2025-10-05', true),

-- Cliente 2
('Supermercado Bom Preço', '(21) 97654-3210', 'compras@bompreco.com.br', 25000.00, 'Varejo Alimentício', 'Revenda', 'Rua das Flores, 250 - Centro, Rio de Janeiro - RJ', '2024-02-20', '2025-10-08', true),

-- Cliente 3
('Construtora Alicerce S/A', '(85) 96543-2109', 'obras@alicerce.com.br', 50000.00, 'Construção Civil', 'Indústria', 'Av. Beira Mar, 450 - Meireles, Fortaleza - CE', '2024-03-10', '2025-10-01', true),

-- Cliente 4
('Clínica Saúde Total', '(11) 95432-1098', 'administrativo@saudetotal.com.br', 10000.00, 'Saúde', 'Consumidor', 'R. Dr. Almeida Lima, 120 - Pinheiros, São Paulo - SP', '2024-04-05', '2025-09-28', true),

-- Cliente 5
('Escola Futuro Brilhante', '(81) 94321-0987', 'diretoria@futurobrilhante.edu.br', 8000.00, 'Educação', 'Consumidor', 'Av. Professor Morais, 300 - Boa Viagem, Recife - PE', '2024-05-12', '2025-10-10', true),

-- Cliente 6
('Restaurante Sabor & Arte', '(11) 93210-9876', 'gerencia@saborarte.com.br', 12000.00, 'Alimentação', 'Revenda', 'R. do Mercado, 45 - Centro, São Paulo - SP', '2024-06-18', '2025-09-15', true),

-- Cliente 7
('Indústria Metal Forte', '(48) 92109-8765', 'suprimentos@metalforte.ind.br', 80000.00, 'Indústria Metalúrgica', 'Indústria', 'Rod. SC-401, Km 12 - Distrito Industrial, Joinville - SC', '2024-07-22', '2025-10-09', true),

-- Cliente 8
('Farmácia Popular', '(21) 91098-7654', 'comercial@farmaciapopular.com.br', 18000.00, 'Farmacêutico', 'Revenda', 'Av. Brasil, 1500 - Madureira, Rio de Janeiro - RJ', '2024-08-14', '2025-10-06', true),

-- Cliente 9
('Academia Corpo e Mente', '(85) 90987-6543', 'recepcao@corpoeamente.com.br', 6000.00, 'Fitness e Bem-estar', 'Consumidor', 'R. do Ginásio, 88 - Aldeota, Fortaleza - CE', '2024-09-08', '2025-09-20', true),

-- Cliente 10
('Escritório Advocacia & Cia', '(11) 89876-5432', 'contato@advocaciaecia.adv.br', 5000.00, 'Serviços Jurídicos', 'Consumidor', 'Av. Faria Lima, 2000 - Itaim Bibi, São Paulo - SP', '2024-10-01', '2025-10-07', true);


-- =====================================================
-- INSERÇÃO DE INTERAÇÕES
-- =====================================================

-- Interações Cliente 1 (Tech Solutions)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(1, 'Telefone', 'Primeiro contato - Cliente interessado em soluções de software empresarial', '2024-01-15 10:30:00'),
(1, 'Email', 'Envio de apresentação institucional e portfólio de produtos', '2024-01-16 14:20:00'),
(1, 'Reunião', 'Reunião presencial para entender necessidades específicas do cliente', '2024-01-22 15:00:00'),
(1, 'WhatsApp', 'Cliente solicitou cotação urgente para sistema de gestão', '2025-10-05 11:15:00');

-- Interações Cliente 2 (Supermercado Bom Preço)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(2, 'Email', 'Cliente solicitou cotação de equipamentos para supermercado', '2024-02-20 09:00:00'),
(2, 'Telefone', 'Esclarecimento de dúvidas sobre prazo de entrega e garantia', '2024-02-25 16:45:00'),
(2, 'Visita', 'Visita técnica ao estabelecimento para avaliar necessidades', '2024-03-05 10:00:00'),
(2, 'Email', 'Cliente aprovou proposta e solicitou início do fornecimento', '2025-10-08 13:30:00');

-- Interações Cliente 3 (Construtora Alicerce)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(3, 'Reunião', 'Apresentação de soluções para obras de grande porte', '2024-03-10 14:00:00'),
(3, 'Email', 'Envio de orçamento detalhado para obra do Shopping Leste', '2024-03-15 10:30:00'),
(3, 'Telefone', 'Negociação de condições de pagamento e prazo de entrega', '2024-03-20 11:00:00');

-- Interações Cliente 4 (Clínica Saúde Total)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(4, 'WhatsApp', 'Cliente interessado em equipamentos médicos', '2024-04-05 09:30:00'),
(4, 'Reunião', 'Apresentação de linha de produtos hospitalares', '2024-04-10 15:30:00'),
(4, 'Email', 'Envio de catálogo e tabela de preços atualizada', '2025-09-28 14:00:00');

-- Interações Cliente 5 (Escola Futuro Brilhante)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(5, 'Telefone', 'Escola precisa de computadores e equipamentos audiovisuais', '2024-05-12 10:00:00'),
(5, 'Email', 'Proposta comercial enviada com condições especiais para educação', '2024-05-18 11:30:00'),
(5, 'Visita', 'Visita à escola para apresentação de produtos', '2025-10-10 09:00:00');

-- Interações Cliente 6 (Restaurante Sabor & Arte)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(6, 'Email', 'Cliente solicitou cotação de equipamentos para cozinha industrial', '2024-06-18 14:30:00'),
(6, 'Telefone', 'Discussão sobre especificações técnicas dos equipamentos', '2024-06-25 16:00:00');

-- Interações Cliente 7 (Indústria Metal Forte)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(7, 'Reunião', 'Negociação de grande contrato de fornecimento', '2024-07-22 10:00:00'),
(7, 'Email', 'Envio de proposta para fornecimento anual', '2024-07-28 09:00:00'),
(7, 'Telefone', 'Cliente aprovou contrato e solicitou início imediato', '2024-08-05 11:00:00'),
(7, 'WhatsApp', 'Acompanhamento de pedido em andamento', '2025-10-09 15:30:00');

-- Interações Cliente 8 (Farmácia Popular)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(8, 'Email', 'Solicitação de parceria para fornecimento de produtos', '2024-08-14 10:30:00'),
(8, 'Reunião', 'Reunião para definir termos de fornecimento regular', '2024-08-20 14:00:00'),
(8, 'Telefone', 'Confirmação de primeira entrega', '2025-10-06 09:15:00');

-- Interações Cliente 9 (Academia Corpo e Mente)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(9, 'WhatsApp', 'Cliente interessado em equipamentos de musculação', '2024-09-08 11:00:00'),
(9, 'Visita', 'Visita à academia para avaliar espaço disponível', '2024-09-15 10:00:00');

-- Interações Cliente 10 (Escritório Advocacia)
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(10, 'Telefone', 'Escritório precisa de mobiliário e equipamentos de TI', '2024-10-01 14:00:00'),
(10, 'Email', 'Envio de catálogo e condições comerciais', '2024-10-03 10:00:00'),
(10, 'Reunião', 'Apresentação presencial e fechamento de negócio', '2025-10-07 16:00:00');


-- =====================================================
-- INSERÇÃO DE COTAÇÕES
-- =====================================================

-- Cotação 1 - Tech Solutions (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-001A', 1, 
'- 5 Licenças de Software de Gestão Empresarial
- 10 Estações de trabalho (computadores)
- Servidor dedicado
- Instalação e configuração
- Treinamento para equipe (40h)', 
45000.00, 'Aprovada', '2024-01-25', '2024-02-25', 'Pagamento em 3x sem juros. Garantia de 12 meses.');

-- Cotação 2 - Supermercado Bom Preço (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-002A', 2,
'- 4 Checkouts completos com leitores de código de barras
- 2 Balanças digitais
- Sistema de gestão de estoque
- 3 Câmeras de segurança
- Instalação e configuração',
32000.00, 'Aprovada', '2024-02-28', '2024-03-31', 'Frete incluso. Instalação em até 15 dias úteis.');

-- Cotação 3 - Construtora Alicerce (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-003A', 3,
'- 500 sacos de cimento CP-II 50kg
- 200 m³ de areia média
- 150 m³ de brita 1
- 50 toneladas de ferro 10mm
- Entrega parcelada conforme cronograma',
85000.00, 'Aprovada', '2024-03-18', '2024-04-18', 'Entregas quinzenais. Pagamento 30 dias após cada entrega.');

-- Cotação 4 - Clínica Saúde Total (ENVIADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-004E', 4,
'- 2 Macas hospitalares elétricas
- 1 Autoclave 21 litros
- 5 Cadeiras para sala de espera
- 1 Armário para medicamentos
- Materiais de consumo (diversos)',
18500.00, 'Enviada', '2024-04-15', '2025-11-15', 'Valores válidos por 30 dias. Frete grátis para São Paulo.');

-- Cotação 5 - Escola Futuro Brilhante (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-005A', 5,
'- 30 Computadores para laboratório de informática
- 1 Projetor Full HD + tela de projeção
- 5 Impressoras multifuncionais
- Software educacional (licenças anuais)
- Instalação e configuração',
52000.00, 'Aprovada', '2024-05-20', '2024-06-20', 'Desconto especial para instituições de ensino. Garantia estendida de 24 meses.');

-- Cotação 6 - Restaurante Sabor & Arte (RECUSADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-006R', 6,
'- 1 Forno industrial a gás
- 1 Fogão industrial 6 bocas
- 2 Fritadeiras elétricas
- 1 Refrigerador vertical 4 portas
- Instalação',
28000.00, 'Recusada', '2024-06-22', '2024-07-22', 'Cliente optou por fornecedor concorrente.');

-- Cotação 7 - Indústria Metal Forte (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-007A', 7,
'- Contrato anual de fornecimento de matéria-prima
- 100 toneladas de aço carbono por mês
- 50 toneladas de alumínio por mês
- Entrega mensal programada
- Condições especiais de preço',
850000.00, 'Aprovada', '2024-08-01', '2024-09-01', 'Contrato de 12 meses renováveis. Reajuste semestral pelo IPCA.');

-- Cotação 8 - Farmácia Popular (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-008A', 8,
'- Fornecimento mensal de medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares
- Equipamentos para farmácia (2x termômetros digitais, oxímetros)
- Condições de pagamento especiais',
22000.00, 'Aprovada', '2024-08-25', '2024-09-25', 'Fornecimento mensal renovável. Primeira entrega em 10 dias.');

-- Cotação 9 - Academia Corpo e Mente (ENVIADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-009E', 9,
'- 10 Esteiras ergométricas
- 5 Bicicletas ergométricas
- Conjunto de pesos e halteres (kit completo)
- 3 Aparelhos de musculação multifuncionais
- Instalação e manutenção por 6 meses',
42000.00, 'Enviada', '2024-09-20', '2025-11-20', 'Parcelamento em até 10x. Garantia de 18 meses para equipamentos.');

-- Cotação 10 - Escritório Advocacia (APROVADA)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-010A', 10,
'- 8 Mesas executivas com gaveteiros
- 8 Cadeiras giratórias ergonômicas
- 5 Armários para arquivos
- 5 Computadores completos
- 2 Impressoras multifuncionais laser
- Rede estruturada e cabeamento',
28500.00, 'Aprovada', '2024-10-05', '2024-11-05', 'Montagem e instalação incluídas. Entrega em 20 dias úteis.');

-- Cotação adicional - Tech Solutions (ENVIADA - segunda cotação)
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-011E', 1,
'- Upgrade do sistema de gestão para versão Enterprise
- 5 Licenças adicionais
- Módulo de Business Intelligence
- Consultoria e customização (80h)',
28000.00, 'Enviada', '2025-10-01', '2025-11-01', 'Proposta de expansão do sistema atual.');


-- =====================================================
-- INSERÇÃO DE PEDIDOS
-- =====================================================

-- Pedido 1 - Tech Solutions (da Cotação 1)
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-001', 1, 1,
'- 5 Licenças de Software de Gestão Empresarial
- 10 Estações de trabalho (computadores)
- Servidor dedicado
- Instalação e configuração
- Treinamento para equipe (40h)',
45000.00, 'Entregue', '2024-02-01', '2024-02-25', '2024-02-22', 'Cliente muito satisfeito. Treinamento concluído com sucesso.');

-- Pedido 2 - Supermercado Bom Preço (da Cotação 2)
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-002', 2, 2,
'- 4 Checkouts completos com leitores de código de barras
- 2 Balanças digitais
- Sistema de gestão de estoque
- 3 Câmeras de segurança
- Instalação e configuração',
32000.00, 'Entregue', '2024-03-05', '2024-03-25', '2024-03-20', 'Instalação realizada fora do horário comercial conforme solicitado.');

-- Pedido 3 - Construtora Alicerce (da Cotação 3) - PRIMEIRA ENTREGA
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-003A', 3, 3,
'Primeira entrega (cronograma):
- 100 sacos de cimento CP-II 50kg
- 40 m³ de areia média
- 30 m³ de brita 1
- 10 toneladas de ferro 10mm',
17000.00, 'Entregue', '2024-03-25', '2024-04-05', '2024-04-03', 'Primeira de cinco entregas programadas.');

-- Pedido 4 - Construtora Alicerce - SEGUNDA ENTREGA
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-003B', 3, 3,
'Segunda entrega (cronograma):
- 100 sacos de cimento CP-II 50kg
- 40 m³ de areia média
- 30 m³ de brita 1
- 10 toneladas de ferro 10mm',
17000.00, 'Enviado', '2024-04-10', '2024-04-20', NULL, 'Previsão de entrega confirmada para 20/04.');

-- Pedido 5 - Escola Futuro Brilhante (da Cotação 5)
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-005', 5, 5,
'- 30 Computadores para laboratório de informática
- 1 Projetor Full HD + tela de projeção
- 5 Impressoras multifuncionais
- Software educacional (licenças anuais)
- Instalação e configuração',
52000.00, 'Em processamento', '2024-06-25', '2024-07-20', NULL, 'Aguardando liberação do setor de logística. Entrega prevista dentro do prazo.');

-- Pedido 6 - Indústria Metal Forte (da Cotação 7) - PRIMEIRA ENTREGA MENSAL
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-007-08', 7, 7,
'Fornecimento mensal - Agosto/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação',
70000.00, 'Entregue', '2024-08-05', '2024-08-30', '2024-08-28', 'Entrega dentro do cronograma. Cliente solicitou manutenção do padrão de qualidade.');

-- Pedido 7 - Indústria Metal Forte - SEGUNDA ENTREGA MENSAL
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-007-09', 7, 7,
'Fornecimento mensal - Setembro/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação',
70000.00, 'Entregue', '2024-09-05', '2024-09-30', '2024-09-29', 'Entrega concluída. Documentação fiscal enviada por email.');

-- Pedido 8 - Indústria Metal Forte - TERCEIRA ENTREGA MENSAL
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-007-10', 7, 7,
'Fornecimento mensal - Outubro/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação',
70000.00, 'Enviado', '2024-10-05', '2024-10-30', NULL, 'Carga despachada. Previsão de chegada em 3 dias úteis.');

-- Pedido 9 - Farmácia Popular (da Cotação 8) - PRIMEIRA ENTREGA
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-008-09', 8, 8,
'Fornecimento mensal - Setembro/2024:
- Medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares
- Equipamentos (termômetros, oxímetros)',
22000.00, 'Entregue', '2024-09-01', '2024-09-10', '2024-09-08', 'Primeira entrega do contrato mensal. Tudo conforme especificado.');

-- Pedido 10 - Farmácia Popular - SEGUNDA ENTREGA
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-008-10', 8, 8,
'Fornecimento mensal - Outubro/2024:
- Medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares',
22000.00, 'Pendente', '2024-10-01', '2024-10-10', NULL, 'Pedido confirmado. Separação em andamento no CD.');

-- Pedido 11 - Escritório Advocacia (da Cotação 10)
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-010', 10, 10,
'- 8 Mesas executivas com gaveteiros
- 8 Cadeiras giratórias ergonômicas
- 5 Armários para arquivos
- 5 Computadores completos
- 2 Impressoras multifuncionais laser
- Rede estruturada e cabeamento',
28500.00, 'Em processamento', '2024-10-08', '2024-10-28', NULL, 'Móveis em produção. Computadores já estão no estoque. Instalação agendada para 28/10.');


-- =====================================================
-- VERIFICAÇÃO DOS DADOS INSERIDOS
-- =====================================================

-- Total de registros por tabela
SELECT 'Clientes' as tabela, COUNT(*) as total FROM clientes
UNION ALL
SELECT 'Interações', COUNT(*) FROM interacoes
UNION ALL
SELECT 'Cotações', COUNT(*) FROM cotacoes
UNION ALL
SELECT 'Pedidos', COUNT(*) FROM pedidos;

-- Resumo de pedidos por status
SELECT status_entrega, COUNT(*) as quantidade, SUM(valor_final) as valor_total
FROM pedidos
GROUP BY status_entrega
ORDER BY quantidade DESC;

-- Resumo de cotações por status
SELECT status, COUNT(*) as quantidade, SUM(valor_total) as valor_total
FROM cotacoes
GROUP BY status
ORDER BY quantidade DESC;

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================