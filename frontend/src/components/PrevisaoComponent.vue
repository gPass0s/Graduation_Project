/* eslint-disable */
<template>
<div class="row justify-content-center">
	<div class="col-md-8">
		<div class="row">
			<div class="col-md-6 mb-3">
				<label for="transacao">Transaction</label>
				<select v-model="transacao" class="form-control custom-select" id="transacao" disabled>
					<option value="venda">Selling or buying</option>
					<option value="aluguel">Location</option>
				</select>
				<div class="invalid-feedback">
					Choose a transaction
				</div>
			</div>

			<div class="col-md-6 mb-3">
				<label for="tipo">Property type</label>
				<select v-model="imovel.tipo" class="form-control custom-select" id="tipo" disabled>
					<option value="casa">House</option>
					<option value="apartamento">Apartment</option>
				</select>
				<div class="invalid-feedback">
					Choose the property type
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col-md-12 mb-3">
				<label for="endereco">Address</label>
				<input v-model="imovel.endereco" type="text" class="form-control" id="endereco" @blur="onEnderecoBlur()">
				<div class="invalid-feedback">
					Por favor, digite um endereço válido
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col-md-12 mb-3">
				{{ endereco }}
			</div>
		</div>

		<hr class="mb-4">

		<div class="row">
			<div class="col-md-6 mb-3">
				<label for="tamanho">Property size</label>
				<div class="input-group">
					<input v-model="imovel.tamanho" type="text" class="form-control" id="tamanho">
					<div class="input-group-append">
						<span class="input-group-text">m&sup2;</span>
					</div>
				</div>
				<div class="invalid-feedback" style="width: 100%;">
					Invalid input
				</div>
			</div>

			<div class="col-md-6 mb-3">
				<label for="quartos">Number of bedrooms</label>
				<input v-model="imovel.quartos" type="number" class="form-control" id="quartos">
				<div class="invalid-feedback">
					Invalid input
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col-md-6 mb-3">
				<label for="banheiros">Number of bathrooms</label>
				<input v-model="imovel.banheiros" type="number" class="form-control" id="banheiros">
				<div class="invalid-feedback">
					Invalid input
				</div>
			</div>

			<div class="col-md-6 mb-3">
				<label for="suites">Number of suites</label>
				<input v-model="imovel.suites" type="number" class="form-control" id="suites">
				<div class="invalid-feedback">
					Invalid input
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col-md-6 mb-3">
				<label for="vagas">Number of parking spaces</label>
				<input v-model="imovel.vagas" type="number" class="form-control" id="vagas">
				<div class="invalid-feedback">
					Invalid input
				</div>
			</div>
		</div>

		<hr class="mb-4">

		<div class="row">
			<div class="col-md-6 mb-3">
				<label for="iptu">IPTU - Property taxes monthly</label>
				<div class="input-group">
					<div class="input-group-prepend">
						<span class="input-group-text">R$</span>
					</div>
					<money v-model="imovel.iptu" class="form-control" id="iptu"></money>
				</div>
				<div class="invalid-feedback" style="width: 100%;">
					Invalid input
				</div>
			</div>

			<div class="col-md-6 mb-3">
				<label for="condominio">Condo fees monthly</label>
				<div class="input-group">
					<div class="input-group-prepend">
						<span class="input-group-text">R$</span>
					</div>
					<money v-model="imovel.condominio" class="form-control" id="condominio"></money>
				</div>
				<div class="invalid-feedback" style="width: 100%;">
					Invalid input
				</div>
			</div>
		</div>

		<hr class="mb-4">

		<button class="btn btn-primary btn-lg btn-block" @click="onSubmit()">Predict (It might take some seconds)</button>

		<div v-if="previsao" class="resultado mt-4 pt-4">
			<h4 class="title">
				This property costs:
			</h4>
			<h1 class="title previsao">
				{{ previsao.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL'}) }}
			</h1>
		</div>
	</div>
</div>
</template>

<script>
    export default {
		name: 'PrevisaoComponent',
		data() {
			return {
				endereco: '',
				transacao: 'venda',
				imovel: {
					tipo: 'apartamento',
					tamanho: null,
					quartos: null,
					banheiros: null,
					suites: null,
					vagas: null,
					iptu: '',
					condominio: '',
					lat: null,
					lng: null,
				},
				previsao: null,
			};
		},

        mounted() {
        },

		methods: {
			onEnderecoBlur()
			{
				if (!this.imovel.endereco.length) return;

				let instance = this.$axios.create();
				delete instance.defaults.headers.common['X-CSRF-TOKEN'];
				delete instance.defaults.headers.common['X-Requested-With'];

				instance.get('https://maps.googleapis.com/maps/api/geocode/json', { params: {address: this.imovel.endereco + ', Belo Horizonte, Minas Gerais, Brasil', key: ''} })
					.then((response) => {
						let results = response.data.results;

						if (results && results.length) {
							this.endereco = results[0].formatted_address;
							this.imovel.lat = results[0].geometry.location.lat;
							this.imovel.lng = results[0].geometry.location.lng;
						}
					});
			},

			onSubmit()
			{
				this.$axios.post('https://cors-anywhere.herokuapp.com/https://us-central1-gpassos-portfolio.cloudfunctions.net/predict', this.imovel, { params: {transacao: this.transacao} })
					.then((response) => {
						this.previsao = response.data;
					});
			}
		},
    }
</script>

<style scoped>
	.resultado {
		text-align: center;
	}
</style>

sudo certbot certonly --webroot -d http://35.199.92.72:80/