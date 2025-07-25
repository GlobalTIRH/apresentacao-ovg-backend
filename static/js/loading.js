document.addEventListener("DOMContentLoaded", function () {
  // Seleciona todos os formulários da página
  const forms = document.querySelectorAll("form");

  forms.forEach(function (form) {
    form.addEventListener("submit", function () {
      // Muda o cursor para loading
      document.body.style.cursor = "wait";

      // Opcional: desabilita o botão de submit para evitar múltiplos envios
      const submitBtn = form.querySelector(
        'button[type="submit"], input[type="submit"]'
      );
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.cursor = "wait";
      }
    });
  });

  // Remove o cursor de loading quando a página carregar completamente
  window.addEventListener("load", function () {
    document.body.style.cursor = "default";
  });
});

function mascaraFone(event) {
  var valor =
    document.getElementById("telefone").attributes[0].ownerElement["value"];
  var retorno = valor.replace(/\D/g, "");
  retorno = retorno.replace(/^0/, "");
  if (retorno.length > 10) {
    retorno = retorno.replace(/^(\d\d)(\d{5})(\d{4}).*/, "($1) $2-$3");
  } else if (retorno.length > 5) {
    if (retorno.length == 6 && event.code == "Backspace") {
      // necessário pois senão o "-" fica sempre voltando ao dar backspace
      return;
    }
    retorno = retorno.replace(/^(\d\d)(\d{4})(\d{0,4}).*/, "($1) $2-$3");
  } else if (retorno.length > 2) {
    retorno = retorno.replace(/^(\d\d)(\d{0,5})/, "($1) $2");
  } else {
    if (retorno.length != 0) {
      retorno = retorno.replace(/^(\d*)/, "($1");
    }
  }
  document.getElementById("telefone").attributes[0].ownerElement["value"] =
    retorno;
}
