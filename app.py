import flet as ft
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Produto


CONN = "sqlite:///projeto.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def main(page: ft.Page):

    # Controle da Janela
    page.title = "Estoque = Generico"
    lista_produtos = ft.ListView(
        expand=1, spacing=10, padding=20, auto_scroll=False)

    # Acoes
    def cadastrar(e):
        try:
            novo_produto = Produto(titulo=produto.value, preco=preco.value)
            session.add(novo_produto)
            session.commit()

            lista_produtos.controls.append(
                ft.Container(ft.Text(p.titulo),
                             bgcolor=ft.colors.BLACK12,
                             padding=15,
                             alignment=ft.alignment.center,
                             margin=3,
                             border_radius=10
                             ))

            print("Produto salvo com sucesso!")
            produto.value = ""
            preco.value = ""
            txt_erro.visible = False
            txt_acerto.visible = True

        except:
            print("Operação Inválida!")
            produto.on_blur = True
            preco.color = ft.colors.RED
            txt_acerto.visible = False
            txt_erro.visible = True

        finally:
            page.update()

    # Componentes
    txt_titulo = ft.Text("Titulo do Produto:")
    produto = ft.TextField(label="Digite o titulo do produto...")

    txt_valor = ft.Text("Preço do Produto")
    preco = ft.TextField(value=0, label="Digite o preco...",
                         text_align=ft.TextAlign.LEFT, prefix_text="R$ ")

    btn_produto = ft.TextButton(text="Sim", on_click=cadastrar)

    # MESSAGENS DO SISTEMA
    txt_acerto = ft.Container(ft.Text("Produto salvo com Sucesso!"), visible=False,
                              bgcolor=ft.colors.GREEN, padding=10, alignment=ft.alignment.center)
    txt_erro = ft.Container(ft.Text("Erro ao salvar o Produto!"), visible=False,
                            bgcolor=ft.colors.RED, padding=10, alignment=ft.alignment.center)

    # Componentes Staticos
    page.add(
        txt_acerto,
        txt_erro,
        txt_titulo,
        produto,

        txt_valor,
        preco,

        btn_produto,


    )

    for p in session.query(Produto).all():
        lista_produtos.controls.append(
            ft.Container(ft.Text(p.titulo),
                         bgcolor=ft.colors.BLACK12,
                         padding=15,
                         alignment=ft.alignment.center,
                         margin=3,
                         border_radius=10
                         ))

    # Componentes Dinamicos
    page.add(
        lista_produtos
    )


ft.app(target=main)
