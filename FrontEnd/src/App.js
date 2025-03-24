import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [menuNavItems, setMenuNavItems] = useState([]);
  const [formData, setFormData] = useState({
    titulo: "",
    conteudo: "",
    publicada: true
  });
  const [scrapingStatus, setScrapingStatus] = useState(""); // Para exibir o status do scraping

  // Função para buscar os itens de menu
  const fetchMenuNavItems = async () => {
    try {
      const response = await axios.get("http://localhost:8000/menu-nav");
      setMenuNavItems(response.data); // Armazenando os dados de menu
    } catch (error) {
      console.error("Erro ao buscar dados:", error);
    }
  };

  // Função para chamar o endpoint de scraping
  const handleScraping = async () => {
    try {
      const response = await axios.get("http://localhost:8000/scrape-ufu");
      setScrapingStatus(response.data.message); // Exibe a quantidade de itens inseridos
      fetchMenuNavItems(); // Atualiza a lista de itens de menu
    } catch (error) {
      console.error("Erro ao executar scraping:", error);
      setScrapingStatus("Erro ao executar scraping.");
    }
  };

  useEffect(() => {
    fetchMenuNavItems(); // Carrega os dados de menu ao montar o componente
  }, []);

  // Função para capturar mudanças nos inputs do formulário
  const handleInputChange = (event) => {
    const value =
      event.target.type === "checkbox" ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value
    });
  };

  // Função para enviar o formulário
  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post("http://localhost:8000/criar", formData); // Envia para o backend
      fetchMenuNavItems(); // Atualiza os dados após envio
      setFormData({
        titulo: "",
        conteudo: "",
        publicada: true
      });
    } catch (error) {
      console.error("Erro ao enviar a mensagem:", error);
    }
  };

  return (
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Mensagens APP
          </a>
        </div>
      </nav>

      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3 mt-3">
            <label htmlFor="titulo" className="form-label">
              Título
            </label>
            <input
              type="text"
              className="form-control"
              id="titulo"
              name="titulo"
              onChange={handleInputChange}
              value={formData.titulo}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="conteudo" className="form-label">
              Conteúdo
            </label>
            <input
              type="text"
              className="form-control"
              id="conteudo"
              name="conteudo"
              onChange={handleInputChange}
              value={formData.conteudo}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="publicada" className="form-label">
              Publicada?
            </label>
            <input
              type="checkbox"
              id="publicada"
              name="publicada"
              onChange={handleInputChange}
              value={formData.publicada}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>

        <h3>Menu de Navegação</h3>
        <table className="table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Texto do Menu</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {menuNavItems.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.menuNav}</td>
                <td>
                  <a href={item.link} target="_blank" rel="noopener noreferrer">
                    {item.link}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Status do scraping */}
        <div>
          <button onClick={handleScraping} className="btn btn-secondary mt-3">
            Executar Scraping
          </button>
          {scrapingStatus && (
            <div className="mt-3">
              <strong>{scrapingStatus}</strong>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
