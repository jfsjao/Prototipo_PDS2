import React, { useState, useEffect } from 'react'
import api from './api'
const App = () => {
  const [Mensagens, setMensagens] = useState([]);
  const [formData, setFormData] = useState({
    titulo: '',
    conteudo: '',
    publicada: true
  })
  const fetchMensagens = async () => {
    const response = await api.get('/mensagens')
    setMensagens(response.data)
  };
  useEffect(() => {
    fetchMensagens();
  }, []);
  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value
    });
  };
  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/criar', formData);
    fetchMensagens();
    setFormData({
      titulo: '',
      conteudo: '',
      publicada: true
    });
  };
  return (
    < div >
      < nav className='navbar navbar-dark bg-primary' >
        < div className='container-fluid' >
          < a className='navbar-brand' href='#' >
            Mensagens APP
          </ a>
        </ div >
      </ nav >
      < div className='container' >
        < form onSubmit={handleFormSubmit}>
          < div className='mb-3 mt-3' >
            < label htmlFor='titulo' className='form-label' >
              Título
            </ label >
            < input type='text' className='form-control' id='titulo' name='titulo' onChange={handleInputChange} value={formData.titulo} />
          </ div >
          < div className='mb-3' >
            < label htmlFor='conteudo' className='form-label' >
              Conteúdo
            </ label >
            < input type='text' className='form-control' id='conteudo' name='conteudo' onChange={handleInputChange} value={formData.conteudo} />
          </ div >
          < div className='mb-3' >
            < label htmlFor='publicada' className='form-label' >
              Publicada?
            </ label >
            < input type='checkbox' id='publicada' name='publicada' onChange={handleInputChange} value={formData.publicada} />
          </ div >
          < button type='submit' className='btn btn-primary' >
            Submit
          </ button >
        </ form >
        < table className='table table-striped table-bordered table-hover' >
          < thead >
            < tr>
              < th>Título</ th>
              < th>Conteúdo</ th>
              < th>Publicada?</ th>
            </ tr>
          </ thead >
          < tbody >
            {Mensagens.map((Mensagem) => (
              < tr key={Mensagem.id}>
                < td>{Mensagem.titulo}</ td>
                < td>{Mensagem.conteudo}</ td>
                < td>{Mensagem.publicada ? 'sim' : 'não'}</ td>
              </ tr>
            ))}
          </ tbody >
        </ table >
      </ div >
    </ div >
  )


}
export default App